# Random-Game-Manager
I made this specifically for Shmoby's "Beating Every Nintendo Published Game" challenge, for anyone who wants to do the challenge but wants to randomize which game you play next, but theoretically, you can replace the games and images and put any games in the program to randomly choose any game. 
                                                    ||
READ THE README if you want to add games or Images. ||
                                                    \/

To Add Games -

  BULK GAME ADDING
      In order to add games in Bulk, the easiest way is to use Google Sheets or Excel. The main thing you need to know is that in the 3 .txt files, all the info about 1 game has to be on the same line in all 3 files. So Line 1 in all the files is the same game. Google Sheets makes this easy,a s you can put all the info across in rows, then copy columns into the respective text files and they'll automatically be formatted correctly.
      So what you want is to put all the Game Names in 1 Column, then next to that, put the Console Information, then next to that, the Release Date. Then you are going to want to copy as follows:
      Game Names Column INTO Games.txt
      Consoles Column INTO Console.txt
      Release Date Column INTO Date.txt 
      Dont worry about Status.txt for now. After you copy those into the txt files, start the program up, and Press the "Reset Games" Button near the top. This will generate the correct number of rows in Status.txt, and now all your games should now be imported correctly.

  SINGLE GAME ADDING
      If you just want to add 1 game at a time, all you have to do is open the program, and click on Edit Table at the bottom, this will open the Table in Edit Mode and allow you to delete any row of the table, and at the top, you can insert the Games Name, Console, and Release Date (MM/DD/YYYY) then Click Add Game. This will Add the game to all the Files automatically.

To Add Pictures - 

  CONSOLE PICTURES
      The Pictures are not shrunk to size automatically, if you put an image that is too large in the folder, the Stats screen will be unreadable. The Images provided for Nintendo Consoles are the correct size, you can use them as reference for how large the images should be.
      In order for the program to use the Images, simply name the Image (.png format only) after the name of the Console provided in the Console.txt
        (So if you labled FDS games as "Famicom Disk System" and not "FDS", then make sure the FDS Image is called, "Famicom Disk System.png")

Lastly, If this program doesnt work for some reason, im sorry, I dont code very often, I tried to make itas best as I could, I'll try and fix any issues that may crop up. Please Enjoy!
