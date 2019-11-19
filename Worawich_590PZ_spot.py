#!/usr/bin/env python

"""
Created on Tue November 7, 2019

This is the final project, Spot game, for IS 590 PZ at UIUC.
I'm doing this alone because I'm lonely.
"""

__author__ = "Worawich Win Chaiyakunapruk"
__copyright__ = "Copyright 2019, Worawich C."
__credits__ = ["John Weible", "https://www.redblobgames.com/grids/hexagons/"]
__version__ = "0.0.3"
__maintainer__ = "Worawich Win Chaiyakunapruk"
__email__ = "wchaiy2@illinois.edu"
__status__ = "Prototype"


import tkinter as tk
import Game_play, AI


EDGE_SIZE = 5
IMG_SPACE = 120
XSPACE = 35 * EDGE_SIZE
YSPACE = 60
WINDOW_HEIGHT = 2 * YSPACE + EDGE_SIZE * IMG_SPACE
WINDOW_WIDTH = 2 * XSPACE + EDGE_SIZE * IMG_SPACE


class GameBoard:
    def __init__(self, frame):
        self.frame = frame
        self.blank = tk.PhotoImage(file="spot/blank.gif")
        self.blue = tk.PhotoImage(file="spot/blue.gif")
        self.yellow = tk.PhotoImage(file="spot/yellow.gif")
        self.green = tk.PhotoImage(file="spot/green.gif")
        self.pink = tk.PhotoImage(file="spot/pink.gif")
        self.make_board()
        self.GamePlay = Game_play.GamePlay()
        self.AI = AI.AI()
        self.loc1 = 0, 0, 0
        self.loc2 = 1, -0, 2
        self.GamePlay.is_adjacent(self.loc1, self.loc2)

    def make_board(self):
        for yi in range(0, EDGE_SIZE):
            xi = XSPACE
            for i in range(0, EDGE_SIZE):
                l = tk.Label(self.frame, image=self.blank)
                l.pack()
                l.image = self.blank
                l.place(anchor=tk.NW, x=xi, y=YSPACE + yi * IMG_SPACE)
                l.bind('<Button-1>', lambda e: self.on_click(e))
                xi += IMG_SPACE

        # make blue base
        l = tk.Label(self.frame, image=self.blue)
        l.image = self.blue
        l.place(anchor=tk.NW, x=XSPACE, y=YSPACE)
        l = tk.Label(self.frame, image=self.blue)
        l.image = self.blue
        l.place(anchor=tk.NW, x=XSPACE + (EDGE_SIZE - 1) * IMG_SPACE, y=YSPACE + (EDGE_SIZE - 1) * IMG_SPACE)


        # make yellow base
        l = tk.Label(self.frame, image=self.yellow)
        l.image = self.yellow
        l.place(anchor=tk.NW, x=XSPACE, y=YSPACE + (EDGE_SIZE - 1) * IMG_SPACE)
        l = tk.Label(self.frame, image=self.yellow)
        l.image = self.yellow
        l.place(anchor=tk.NW, x=XSPACE + (EDGE_SIZE - 1) * IMG_SPACE, y=YSPACE)

        # Start game with yellow turn
        l = tk.Label(self.frame, text="Current turn: yellow")
        l.place(anchor=tk.NW)

    def get_location(self, widget):
        row = (widget.winfo_y() - YSPACE) / IMG_SPACE
        col = (widget.winfo_x() - XSPACE) / IMG_SPACE
        col, row = int(col), int(row)
        print(widget.winfo_x(), widget.winfo_y())
        print(col, row)
        self.make_coordinate(col, row)
        return col, row

    def make_coordinate(self, x_location, y_location):
        y_coor = y_location * IMG_SPACE + YSPACE
        x_coor = x_location * IMG_SPACE + XSPACE
        x_coor, y_coor = int(x_coor), int(y_coor)
        print(x_location, y_location)
        print(x_coor, y_coor)
        return x_coor, y_coor

    def get_coordinates(self, widget):
        x, y = self.get_location(widget)
        x, y = int(x), int(y)
        print(x, y)
        return x, y

    def toggle_color(self, widget):
        if self.GamePlay.turn == 1:
            widget.config(image=self.blue)
            widget.image = self.blue
            l = tk.Label(self.frame, text="Current turn: yellow")
            l.place(anchor=tk.NW)
            x, y = self.get_coordinates(widget)

            self.GamePlay.make_history(x, y)
            # # check edge to copy dot
            # mirror_x_2d, mirror_y_2d = self.mirror_location_2d(x_2d, y_2d)
            # mirror_x_3d, mirror_y_3d, mirror_z_3d = self.axial_to_cube(mirror_x_2d, mirror_y_2d)
            # lo_x, lo_y = self.make_location_3d(mirror_x_3d, mirror_y_3d, mirror_z_3d)
            # # make copied dot visualized
            # l = tk.Label(self.frame, image=self.blue)
            # l.image = self.blue
            # l.place(anchor=tk.NW, x=lo_x, y=lo_y)

        else:
            widget.config(image=self.yellow)
            widget.image = self.yellow
            l = tk.Label(self.frame, text="Current turn:  blue  ")
            l.place(anchor=tk.NW)
            x, y = self.get_coordinates(widget)

            self.GamePlay.make_history(x, y)

    def on_click(self, event):
        print(self.GamePlay.turn)
        if event.widget.image == self.blank:
            return
        elif event.widget.image == self.yellow:
            print("HERE")
            self.toggle_color(event.widget)
        # x, y, z = self.get_coordinates(event.widget)
        # print(x, y, z)
        # if is_game_complete():
        #     self.quit()
        self.GamePlay.turn = (self.GamePlay.turn + 1) % 2


class GameWindow:
    def __init__(self, window):
        self.frame = tk.Frame(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.frame.pack()
        self.GameBoard = GameBoard(self.frame)


if __name__ == '__main__':
    window = tk.Tk()
    window.wm_title("TetraHex")
    GameWindow(window)
    window.mainloop()



