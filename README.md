# SaveNLoad
A Python script to load WC3 save files made with Guhun's Save/Load system


How does it work?
The program's main loop periodically checks your Wacraft III directory to find a load.txt file that has been created using the in-game -request command.

## Features

 - **Autoupdates**
 No need to check for updates, the program will automatically check for new updates on GitHub and update itself. You can disable this in the settings text files.

- **Read save files from GitHub**
If you supply a GitHub repository, and it is structured like a SaveNLoad saves folder, then you will be able to load files from that repository.

- **Interaction with WC3**
There is no need to alt-tab to load your saves! Just leave SaveNLoad.exe running in the backround and send request commands from the game.

## Save Folder Structure

Each save made by the user is actually a directory (folder). Inside it, there are many numbered files, from **0.txt** onward. The total ammount of files is saved in a separate file, called **size.txt**. If the size file is missing, the save will be considered corrupted and will not be loaded. If any of the numbered files is missing, an error message will appear on the console, but the program will continue normally.

Other files: 
**center.txt** => stores the center of a save file. This is only used by Warcraft III, though currently it has no implementation.
**version.txt** => stores the major version of Guhun's SaveNLoad system which was used to create the save. If this file is not found, the program will assume that the version used was 1. Major versions indicate changes to the internal structure of the save files. Thus, you will need a **SaveNLoad.exe** of the same major verison or higher to load a save.

## Cloud Saving
It is possible to load save files from a GitHub repository. Normally, you can find your save files in the path: **C:\Users\Username\Documents\Warcraft III\CustomMapData\Data Manager\\**. If you want to create a save repostiory on GitHub, it must be structured like that folder. You can find an example here: https://github.com/Son-Guhun/SnL-Cloud-Test

You must configure your SaveNLoad to load files from a GitHub Repostiory. To do so, you must open the **Settings** folder that is created after you run **SaveNLoad.exe** and find the **GitHub-Repository.txt** file. If one does not exist, then you can create it. The contents of the file must be a single line in the form of: */GitHubUserName/Repository*.
Example: */Son-Guhun/SnL-Cloud-Test*
