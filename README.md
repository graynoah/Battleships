# Battleships

## Game Description

Battleships is a guessing game with some strategy-type elements. Our game can be played between two players (people), or between a player and a computer. The game is played on a grid, at the start of the game players place their ships on their respective grids. A ship can cover multiple spots on the grid, and ships are hidden from the view of the other player. The game progresses in turns, switching between players and allowing them to take a "shot" at the other players grid, in an attempt to hit the location of their hidden ships. The location of hit and missed shots are displayed on the grid for players to see. Once all spots on that ship are hit, the ship becomes sunk. Once all the player's ships are sunk, the game is over and the player with ships remaining unsunk wins!

## Screenshots

TBD

## Game Controls and Features

Battleships allows you to customize the game settings to your preference. For instance, the settings menu will allow you to choose to play in full screen and change the sound volume to your liking. A user can also pause the game at any point with the pause menu and resume the game when it is convenient. Moreover, Battleships has a Human vs Computer feature in addition to playing a Human vs Human game. Therefore, the user can choose who they want to play with at the beginning of the game.

## How to Install the Battleship

To install the game, download
[Python 3.8.0](https://www.python.org/ftp/python/3.8.0/python-3.8.0.exe). Once downloaded open a terminal and run pip install pygame.
After that is done downloading and installing, change to you desired install directory using cd \[desired directory\]. Then clone our repository by doing git clone https://github.com/graynoah/Battleships.git. Once it is done downloading, you will see a folder called Battleships appear in your desired directory, run the main.py file inside the folder to play the game.

## Documentation and Directory Structure

The Battleships repository contains subfolders to organize the code.
The _Audio_ folder contains all the sound and music files used in Battleships. Similarly, the Images folder contains pictures used in the game. The _Players_ folder contains the different types of players: the abstract _Player_, _HumanPlayer_ and _ComputerPlayer_. The _ComputerPlayer_, for instance, is implemented with the Random strategy: on its turn, the computer will make a random shot at the opponent ships. Since a _Ship_ object is a crucial playing piece in this game, the _Ship_ class was added to _Players_ as well. The _Components_ folder has all the components that make up our graphic user interface: buttons, animated grids, backgrounds, etc. There are also different managers, such as the _AudioManager_, which are located in the _Managers_ folder. Each manager helps control an aspect of the game. For instance, the _AudioManager_ is controlling the sound in Battleships. Moreover, each scene in the _Scenes_ folder is responsible for the screen display throughout the game. Finally, the _util_ folder contains design patterns, such as the Observer pattern, that were used to design the game.

An important class that could be extended is the _ComputerPlayer_ class. Currently there is a Random strategy for making a move; a better idea could be a "Greedy" strategy. A Greedy strategy would aim to hit an opponent ship on every move. One idea is to spread out the hits rather than shooting in the same area every time. That way, the player can cover as much area on the board as possible, which increases the chance of hitting an opponent ship.

## Authors

Team Deer consists of 4 members, of which three are 2nd-year, one is 3rd-year, at the University of Toronto Mississauga.
This project was done for credit in the course [CSC290](https://student.utm.utoronto.ca/calendar/course_detail.pl?Depart=7&Course=CSC290H5).
Group members are listed below:

-   Nimra Aftab
-   Julian de Rushe
-   Jicun Zhou
-   Noah Hamilton Gray

## Addendum

**Jicun​** - I was responsible for completing the basic game logic, main menu and pause menu.
Besides, I designed the structure of the project README and filled in Authors and License
Information.

**Julian** - I created the gui framework used in the game. I also created the installation instructions in the README.

**Noah** - I created the computer player, designing and implementing it's strategy to play the game. As well as coming
up with the game description in the README.

**Nimra** - I made an audio manager to play sounds / music in the game. As part of making the manager, I searched for audio files online that we could use in our game. The audio files I added were: background music, "ship hit" sound effect and "canon shot" sound effect. Then, I made methods in the manager that will load the audio files and play or stop them as needed. I also made an abstract player class which indicates the attributes that all players in this game must have. In addition, I helped design the setting menu page. In the settings menu, I chose a good background color scheme and designed buttons that allow the user to customize the game. For example, I designed a label for the sound volume and positioned a slider to change the volume.
To the README, I contributed to "Game Controls and Features". More specifically, I mentioned that users can control music volume, fullscreen mode and opponent type. Finally, I completed the entire paragraph on documentation and provided a suggestion for how others can extend our game.

## License Information

The MIT License (MIT)

Copyright © 2019 Deer

You can find the License [here](https://github.com/graynoah/Battleships/blob/master/LICENSE).
