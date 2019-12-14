# Spot [in progress]

## Current known problem:
Minimax with alpha-beta pruning is inversed. It target the worst score instead of the best.<br>
There will be the settings gui that let you adjust the board, number of players, and hardness. (Functions work but GUI under construction)<br>

## Background

Different implementations of Dave Crummack and Craig Galley's 1988 take (as Infection) on Othello, sharing superficial similarities of the domination of a small grid gameboard by pieces featuring one of two colours... with variant gameboard shapes and layouts possible as per the popular Hexxagōn flavour.

The rules can be summarized as follows: each turn, a player can either move one of his pieces two spaces away, or clone one of his pieces onto a neighboring cell. If the newly moved or cloned piece ends up adjacent to some enemy pieces, it converts them into its color so that they go under the player's control.


## Approach

I use Tkinter to make the board by using a grid of spot pictures (simply Paint it). There are 5 difference colors of spot pictures, red, blue, green, yellow, and empty spot, which I swap them on click. As the click function triggered, it also returns the coordinate of the TK windows and transposes back to x, y coordinate to use with the logical gameplay functions. The UI of the board is done and working properly. There are many functions to transpose back and forward between the UI and the logical coordinates. 


## Usage

To play in 2-player mode, just run the Main_board.py
Run the Game_play.py for random against AI (for testing).
*No need to install requirements. All packages used are essentials.*


## Options<br>
#### AI modes<br>
Easy mode - random<br>
Medium - 1 layer look ahead<br>
Hard - minimax with alpha-beta pruning<br>
#### Multiplayer<br>
2-player <br>
4-player <br>
You will be able to choose from 1-4 human players and fill in the rest with AI player.<br>
#### Board size<br>
The board will be a square from 5x5 and larger<br>

## Gameplay pictures:<br>
For 5x5:<br>
<img src="https://github.com/winwowin/590PZ-Project/blob/master/game1.png?raw=true" width="70%" height="70%" /><br><br>

For 7x7:<br>

<img src="https://github.com/winwowin/590PZ-Project/blob/master/game2.png?raw=true" width="70%" height="70%" />
