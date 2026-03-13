import tkinter as tk
from tkinter import ttk, messagebox
import random
import os
from datetime import datetime

GAMES_FILE = "Games.txt"
CONSOLES_FILE = "Console.txt"
DATES_FILE = "Date.txt"
STATUS_FILE = "Status.txt"

def load_file(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f]

def save_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        for line in data:
            f.write(line + "\n")

def load_data():
    games = load_file(GAMES_FILE)
    consoles = load_file(CONSOLES_FILE)
    dates = load_file(DATES_FILE)
    status = load_file(STATUS_FILE)
    if len(status) < len(games):
        status += ["Not Played"] * (len(games) - len(status))
    return list(zip(games, consoles, dates, status))

def save_data(data):
    games, consoles, dates, status = zip(*data)
    save_file(GAMES_FILE, games)
    save_file(CONSOLES_FILE, consoles)
    save_file(DATES_FILE, dates)
    save_file(STATUS_FILE, status)

class GameManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Manager")
        self.data = load_data()
        self.display_data = self.data.copy()
        self.sort_state = {"Game": True, "Console": True, "Release Date": True, "Status": True}
        self.edit_mode = False

        self.top_frame = tk.Frame(root, pady=10)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        self.top_buttons_frame = tk.Frame(self.top_frame)
        self.top_buttons_frame.pack(anchor="center")

        self.roll_button = tk.Button(self.top_buttons_frame, text="Roll Next Game", command=self.roll_game, font=("Arial", 14))
        self.roll_button.grid(row=0, column=0, padx=5)

        self.beaten_button = tk.Button(self.top_buttons_frame, text="Mark as Beaten", command=self.mark_beaten, font=("Arial", 14))
        self.beaten_button.grid(row=0, column=1, padx=5)
        self.beaten_button.grid_remove()

        self.reset_button = tk.Button(self.top_buttons_frame, text="Reset Games", command=self.reset_games, font=("Arial", 14))
        self.reset_button.grid(row=0, column=2, padx=20)

        self.current_game_frame = tk.Frame(self.top_frame)
        self.current_game_frame.pack(pady=5, anchor="center")

        self.console_frame = tk.Frame(self.current_game_frame)
        self.console_frame.pack(side=tk.LEFT, padx=10, anchor="s")

        self.current_console_label = tk.Label(self.console_frame, text="", font=("Arial", 14))
        self.current_console_label.pack(anchor="s")

        self.current_game_label = tk.Label(self.current_game_frame, text="", font=("Arial", 18, "bold"))
        self.current_game_label.pack(side=tk.LEFT, padx=10)

        self.year_frame = tk.Frame(self.current_game_frame)
        self.year_frame.pack(side=tk.LEFT, padx=10, anchor="s")

        self.current_year_label = tk.Label(self.year_frame, text="", font=("Arial", 12))
        self.current_year_label.pack(anchor="s")

        self.bottom_frame = tk.Frame(root, pady=10)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.table_btn = tk.Button(self.bottom_frame, text="View Table", command=self.show_table)
        self.table_btn.pack(side=tk.LEFT, padx=10)

        self.stats_btn = tk.Button(self.bottom_frame, text="View Stats", command=self.show_stats)
        self.stats_btn.pack(side=tk.LEFT, padx=10)

        self.edit_btn = tk.Button(self.bottom_frame, text="Edit Table", command=self.enter_edit_mode)
        self.edit_btn.pack(side=tk.LEFT, padx=10)
        self.table_btn.config(state="disabled")  
        self.stats_btn.config(state="normal")
        self.edit_btn.config(state="normal")

        self.middle_frame = tk.Frame(root)
        self.middle_frame.pack(fill=tk.BOTH, expand=True)

        self.table_frame = tk.Frame(self.middle_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        self.columns = ("Game", "Console", "Release Date", "Status")

        self.tree_scroll = ttk.Scrollbar(self.table_frame, orient="vertical")
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=self.columns + ("Delete",),
            show="headings",
            yscrollcommand=self.tree_scroll.set
        )
        self.tree_scroll.config(command=self.tree.yview)

        for col in self.columns:
            self.tree.heading(col, text=col + " ↑", command=lambda _col=col: self.sort_column(_col))
        self.tree.column("Game", width=750)
        self.tree.column("Console", width=200, anchor="center")
        self.tree.column("Release Date", width=150, anchor="center")
        self.tree.column("Status", width=150, anchor="center")
        self.tree.column("Delete", width=5, anchor="center")
        self.tree.heading("Delete", text="🗑️")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.stats_frame = tk.Frame(self.middle_frame)

        self.stats_canvas = tk.Canvas(self.stats_frame)
        self.stats_scrollbar = ttk.Scrollbar(self.stats_frame, orient="vertical", command=self.stats_canvas.yview)
        self.stats_canvas.configure(yscrollcommand=self.stats_scrollbar.set)

        self.stats_inner = tk.Frame(self.stats_canvas)
        self.stats_canvas.create_window((0,0), window=self.stats_inner, anchor="nw")

        self.stats_inner.bind(
            "<Configure>",
            lambda e: self.stats_canvas.configure(scrollregion=self.stats_canvas.bbox("all"))
        )

        self.stats_canvas.pack(side="left", fill="both", expand=True)
        self.stats_scrollbar.pack(side="right", fill="y")

        self.stats_images = {}

        self.refresh_table()
        self.update_current_game_label()

        self.tree.bind("<Double-1>", self.edit_cell)
        self.tree.bind("<Button-1>", self.check_delete_click)

    def update_current_game_label(self):
        playing = [g for g in self.data if g[3] == "Playing"]
        if playing:
            game = playing[0]
            self.current_console_label.config(text=game[1])
            self.current_game_label.config(text=game[0])
            year = game[2].split('/')[-1] if game[2] else "N/A"
            self.current_year_label.config(text=year)
            self.roll_button.grid_remove()
            self.beaten_button.grid()
        else:
            self.current_console_label.config(text="")
            self.current_game_label.config(text="")
            self.current_year_label.config(text="")
            self.beaten_button.grid_remove()
            self.roll_button.grid()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for game, console, date, status in self.display_data:
            values = (game, console, date, status)
            if self.edit_mode:
                values = values + ("🗑️",)
            self.tree.insert("", tk.END, values=values)

    def sort_column(self, col):
        if self.edit_mode:
            return
        col_index = {"Game":0,"Console":1,"Release Date":2,"Status":3}[col]
        ascending = self.sort_state[col]
        if col=="Release Date":
            self.display_data.sort(
                key=lambda x: datetime.strptime(x[col_index], "%m/%d/%Y") if x[col_index] else datetime.min,
                reverse=not ascending
            )
        else:
            self.display_data.sort(
                key=lambda x: x[col_index].lower(),
                reverse=not ascending
            )
        self.sort_state[col] = not ascending
        for c in ("Game","Console","Release Date","Status"):
            arrow = "↑" if c==col and ascending else "↓" if c==col else "↑"
            self.tree.heading(c, text=c+" "+arrow)
        self.refresh_table()

    def roll_game(self):
        playing = [g for g in self.data if g[3]=="Playing"]
        if playing:
            messagebox.showinfo("Already Playing", f"You're already playing {playing[0][0]}")
            return
        available = [g for g in self.data if g[3]=="Not Played"]
        if not available:
            messagebox.showinfo("No Games Left", "No unplayed games available!")
            return
        game = random.choice(available)
        self.data = [(g[0], g[1], g[2], "Playing") if g==game else g for g in self.data]
        save_data(self.data)
        self.display_data = self.data.copy()
        self.refresh_table()
        self.update_current_game_label()
        if self.stats_frame.winfo_ismapped():
            self.draw_stats()

    def mark_beaten(self):
        playing = [g for g in self.data if g[3]=="Playing"]
        if not playing:
            messagebox.showinfo("No Game", "No game is currently being played.")
            return
        game = playing[0]
        self.data = [(g[0], g[1], g[2], "Beaten") if g==game else g for g in self.data]
        save_data(self.data)
        self.display_data = self.data.copy()
        self.refresh_table()
        self.update_current_game_label()
        if self.stats_frame.winfo_ismapped():
            self.draw_stats()
        messagebox.showinfo("Marked as Beaten", f"{game[0]} has been marked as beaten!")

    def reset_games(self):
        confirm = messagebox.askyesno("Reset Games", "Are you sure you want to reset all beaten games?")
        if confirm:
            self.data = [(g[0], g[1], g[2], "Not Played") for g in self.data]
            save_data(self.data)

            num_rows = len(self.data)
            with open(STATUS_FILE, "w", encoding="utf-8") as f:
                for _ in range(num_rows):
                    f.write("Not Played\n")

            self.display_data = self.data.copy()
            self.refresh_table()
            self.update_current_game_label()
            if self.stats_frame.winfo_ismapped():
                self.draw_stats()
            messagebox.showinfo("Reset Complete", "All games have been reset to Not Played.")

    def show_table(self):
        self.stats_frame.pack_forget()
        self.table_frame.pack(fill=tk.BOTH, expand=True)
        if self.edit_mode:
            self.destroy_edit_mode()

        self.table_btn.config(state="disabled")
        self.stats_btn.config(state="normal")
        self.edit_btn.config(state="normal")

    def show_stats(self):
        if self.edit_mode:
            self.destroy_edit_mode()

        self.stats_btn.config(state="disabled")
        self.table_btn.config(state="normal")
        self.edit_btn.config(state="normal")

        self.table_frame.pack_forget()
        self.stats_frame.pack(fill=tk.BOTH, expand=True)

        self.root.after(10, self.draw_stats)

    def draw_stats(self):
        for w in self.stats_inner.winfo_children():
            w.destroy()
        counts = {}
        earliest = {}
        for g,c,d,s in self.data:
            if c not in counts:
                counts[c] = {"Beaten":0,"Total":0}
                earliest[c] = datetime.strptime(d,"%m/%d/%Y") if d else datetime.max
            counts[c]["Total"] += 1
            if s=="Beaten":
                counts[c]["Beaten"] += 1
            game_date = datetime.strptime(d,"%m/%d/%Y") if d else datetime.max
            if game_date < earliest[c]:
                earliest[c] = game_date
        sorted_consoles = sorted(counts.keys(), key=lambda c: earliest[c])
        num_cols = 8
        box_width = 160
        box_height = 160
        row=0
        col=0
        self.stats_images = {}
        for console in sorted_consoles:
            cframe = tk.Frame(self.stats_inner, width=box_width, height=box_height, bd=1, relief=tk.SOLID)
            cframe.grid(row=row, column=col, padx=10, pady=10)
            cframe.grid_propagate(False)
            cframe.update()
            inner = tk.Frame(cframe, width=box_width, height=box_height)
            inner.pack(expand=True)
            inner.pack_propagate(False)
            img_path = f"{console}.png"
            if os.path.exists(img_path):
                try:
                    photo = tk.PhotoImage(file=img_path)
                    self.stats_images[console] = photo
                    tk.Label(inner, image=photo).pack(pady=5)
                except tk.TclError:
                    tk.Label(inner, text="Image error").pack(pady=5)
            tk.Label(inner,text=console,font=("Arial",14)).pack()
            progress = ttk.Progressbar(inner,length=150,maximum=counts[console]["Total"])
            progress['value']=counts[console]["Beaten"]
            progress.pack(pady=5)
            tk.Label(inner,text=f"{counts[console]['Beaten']} / {counts[console]['Total']}").pack()
            col += 1
            if col >= num_cols:
                col = 0
                row += 1
        for i in range(num_cols):
            self.stats_inner.grid_columnconfigure(i, weight=1)

    def enter_edit_mode(self):
        self.stats_frame.pack_forget()
        self.table_frame.pack(fill=tk.BOTH, expand=True)
        if self.edit_mode:
            return
    
        self.edit_mode = True
        self.current_game_frame.pack_forget()
        self.top_buttons_frame.pack_forget()

        self.edit_btn.config(state="disabled")
        self.table_btn.config(state="normal")
        self.stats_btn.config(state="normal")

        if hasattr(self, 'add_frame'):
            self.add_frame.destroy()

        self.add_frame = tk.Frame(self.top_frame)
        self.add_frame.pack(pady=5)

        tk.Label(self.add_frame, text="Name:").grid(row=0,column=0)
        tk.Label(self.add_frame, text="Console:").grid(row=0,column=2)
        tk.Label(self.add_frame, text="Release Date:").grid(row=0,column=4)

        self.name_entry = tk.Entry(self.add_frame)
        self.console_entry = tk.Entry(self.add_frame)
        self.date_entry = tk.Entry(self.add_frame)

        self.name_entry.grid(row=0,column=1)
        self.console_entry.grid(row=0,column=3)
        self.date_entry.grid(row=0,column=5)

        self.add_button = tk.Button(self.add_frame, text="Add Game", command=self.add_game, state="disabled")
        self.add_button.grid(row=0,column=6, padx=10)

        self.name_entry.bind("<KeyRelease>", self.check_add_fields)
        self.console_entry.bind("<KeyRelease>", self.check_add_fields)
        self.date_entry.bind("<KeyRelease>", self.check_add_fields)

        self.refresh_table()

    def destroy_edit_mode(self):
        self.edit_mode = False
        if hasattr(self, 'add_frame'):
            self.add_frame.destroy()
        self.top_buttons_frame.pack(anchor="center")
        self.current_game_frame.pack(pady=5, anchor="center")
        self.refresh_table()
        self.update_current_game_label()

    def check_add_fields(self,event=None):
        if self.name_entry.get() and self.console_entry.get() and self.date_entry.get():
            self.add_button.config(state="normal")
        else:
            self.add_button.config(state="disabled")

    def add_game(self):
        name = self.name_entry.get()
        console = self.console_entry.get()
        date = self.date_entry.get()
        confirm = messagebox.askyesno(
            "Confirm Add",
            f"Are you sure you want to add this game?\n\nName: {name}\nConsole: {console}\nRelease Date: {date}"
        )
        if confirm:
            self.data.append((name, console, date, "Not Played"))
            self.data.sort(key=lambda x: datetime.strptime(x[2], "%m/%d/%Y") if x[2] else datetime.max)
            save_data(self.data)
            self.display_data = self.data.copy()
            self.refresh_table()
            self.name_entry.delete(0,tk.END)
            self.console_entry.delete(0,tk.END)
            self.date_entry.delete(0,tk.END)
            self.add_button.config(state="disabled")
            
    def edit_cell(self,event):
        if not self.edit_mode:
            return
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        row_id = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        col_index = int(col.replace('#','')) -1
        if col_index >= len(self.columns):
            return
        x,y,width,height = self.tree.bbox(row_id, col)
        value = self.tree.set(row_id, self.columns[col_index])
        entry = tk.Entry(self.tree)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0,value)
        entry.focus()
        def save_edit(event=None):
            new_val = entry.get()
            entry.destroy()
            self.tree.set(row_id, self.columns[col_index], new_val)
            idx = self.tree.index(row_id)
            data_row = list(self.data[idx])
            data_row[col_index] = new_val
            self.data[idx] = tuple(data_row)
            save_data(self.data)
        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", save_edit)

    def check_delete_click(self,event):
        if not self.edit_mode:
            return
        row_id = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        if col != f"#{len(self.columns)+1}":
            return
        idx = self.tree.index(row_id)
        confirm = messagebox.askyesno(
            "Delete Game",
            f"Are you sure you want to delete '{self.data[idx][0]}'?"
        )
        if confirm:
            self.data.pop(idx)
            save_data(self.data)
            self.display_data = self.data.copy()
            self.refresh_table()

if __name__=="__main__":
    root = tk.Tk()
    root.geometry("1900x800")
    app = GameManagerApp(root)
    root.mainloop()