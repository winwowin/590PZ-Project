# Spot [in progress]


Background

Different implementations of Dave Crummack and Craig Galley's 1988 take (as Infection) on Othello, sharing superficial similarities of the domination of a small grid gameboard by pieces featuring one of two colours... with variant gameboard shapes and layouts possible as per the popular Hexxagōn flavour.

The rules can be summarized as follows: each turn, a player can either move one of his pieces two spaces away, or clone one of his pieces onto a neighboring cell. If the newly moved or cloned piece ends up adjacent to some enemy pieces, it converts them into its color so that they go under the player's control.


Approach

I use Tkinter to make the board by using a grid of spot pictures (simply Paint it). There are 5 difference colors of spot pictures, red, blue, green, yellow, and empty spot, which I swap them on click. As the click function triggered, it also returns the coordinate of the TK windows and transposes back to x, y coordinate to use with the logical gameplay functions. The UI of the board is done and working properly. There are many functions to transpose back and forward between the UI and the logical coordinates. Gameplay part still need to be implemented.


Gameplay pictures:<br>
![Board1](https://github.com/winwowin/590PZ-Project/blob/master/game1.png?raw=true | width=50)

![Board2](https://github.com/winwowin/590PZ-Project/blob/master/game2.png?raw=true =250x250)
