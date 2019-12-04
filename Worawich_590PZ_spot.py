#!/usr/bin/env python

"""
Created on Tue November 7, 2019

This is the final project, Spot game, for IS 590 PZ at UIUC.
I'm doing this alone because I'm lonely.
"""

__author__ = "Worawich Win Chaiyakunapruk"
__copyright__ = "Copyright 2019, Worawich C."
__credits__ = ["John Weible"]
__version__ = "0.0.3"
__maintainer__ = "Worawich Win Chaiyakunapruk"
__email__ = "wchaiy2@illinois.edu"
__status__ = "Prototype"


import tkinter as tk
import Game_play
# import AI


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
        self.GamePlay = Game_play.GamePlay(EDGE_SIZE)
        # self.AI = AI.AI()
        self.click_num = 0
        self.x = -1
        self.y = -1
        self.x2 = -1
        self.y2 = -1

    def make_board(self):
        for yi in range(0, EDGE_SIZE):
            xi = XSPACE
            for i in range(0, EDGE_SIZE):
                l = tk.Label(self.frame, image=self.blank)
                l.pack()
                # create board
                l.image = self.blank
                l.place(anchor=tk.NW, x=xi, y=YSPACE + yi * IMG_SPACE)
                # bind + trigger the click function
                l.bind('<Button-1>', lambda e: self.on_click(e))
                xi += IMG_SPACE


    # def make_base(self):
        # make blue base
        l = tk.Label(self.frame, image=self.blue)
        l.image = self.blue
        l.place(anchor=tk.NW, x=XSPACE, y=YSPACE)
        l.bind('<Button-1>', lambda e: self.on_click(e))

        l = tk.Label(self.frame, image=self.blue)
        l.image = self.blue
        l.place(anchor=tk.NW, x=XSPACE + (EDGE_SIZE - 1) * IMG_SPACE, y=YSPACE + (EDGE_SIZE - 1) * IMG_SPACE)
        l.bind('<Button-1>', lambda e: self.on_click(e))

        # make yellow base
        l = tk.Label(self.frame, image=self.yellow)
        l.image = self.yellow
        l.place(anchor=tk.NW, x=XSPACE, y=YSPACE + (EDGE_SIZE - 1) * IMG_SPACE)
        l.bind('<Button-1>', lambda e: self.on_click(e))

        l = tk.Label(self.frame, image=self.yellow)
        l.image = self.yellow
        l.place(anchor=tk.NW, x=XSPACE + (EDGE_SIZE - 1) * IMG_SPACE, y=YSPACE)
        l.bind('<Button-1>', lambda e: self.on_click(e))

        # Start game with yellow turn
        l = tk.Label(self.frame, text="Current turn: yellow")
        l.place(anchor=tk.NW)

    def get_location(self, widget):
        """Get board coordinate as x, y"""

        row = (widget.winfo_y() - YSPACE) / IMG_SPACE
        col = (widget.winfo_x() - XSPACE) / IMG_SPACE
        col, row = int(col), int(row)
        # print(widget.winfo_x(), widget.winfo_y())
        # print(col, row)
        self.make_coordinate(col, row)
        return col, row

    def make_coordinate(self, x_location, y_location):
        """Get Window's coordinate as pixels"""

        y_coor = y_location * IMG_SPACE + YSPACE
        x_coor = x_location * IMG_SPACE + XSPACE
        x_coor, y_coor = int(x_coor), int(y_coor)
        # print(x_location, y_location)
        # print(x_coor, y_coor)
        return x_coor, y_coor

    def get_coordinates(self, widget):
        x, y = self.get_location(widget)
        x, y = int(x), int(y)
        # print(x, y)
        return x, y

    def toggle_color(self, widget):
        if self.GamePlay.turn == 1:
            widget.config(image=self.blue)
            widget.image = self.blue
            l = tk.Label(self.frame, text="Current turn: yellow")
            l.place(anchor=tk.NW)
            # x, y = self.get_coordinates(widget)
            self.GamePlay.update_board(self.x2, self.y2)

            self.GamePlay.make_history(self.x, self.y, self.x2, self.y2)  # Need to make remove_history mechanism

        else:
            widget.config(image=self.yellow)
            widget.image = self.yellow
            l = tk.Label(self.frame, text="Current turn:  blue  ")
            l.place(anchor=tk.NW)
            # x, y = self.get_coordinates(widget)
            self.GamePlay.update_board(self.x2, self.y2)
            self.GamePlay.make_history(self.x, self.y, self.x2, self.y2)  # Need to make remove_history mechanism

    def delete_color(self, widget):
        x_window, y_window = self.make_coordinate(self.x, self.y)
        # print(x_window, y_window)
        l = tk.Label(self.frame, image=self.blank)
        l.image = self.blank
        l.place(anchor=tk.NW, x=x_window, y=y_window)
        self.GamePlay.update_board(self.x2, self.y2)
        self.GamePlay.remove_move_on_board(self.x, self.y)
        self.GamePlay.make_history(self.x, self.y, self.x2, self.y2)  # Need to make remove_history mechanism
        print(self.GamePlay.get_history())

    def invade_color(self, widget):
        invade_list = self.GamePlay.invade(self.x2, self.y2)
        for oppo_location in invade_list:
            x_new, y_new = oppo_location
            x_window, y_window = self.make_coordinate(x_new, y_new)
            if self.GamePlay.turn == 1:
                # color = self.blue
                widget.config(image=self.blue)
                widget.image = self.blue
                l = tk.Label(self.frame, image=self.blue)
                l.place(anchor=tk.NW, x=x_window, y=y_window)
            else:
                # color = self.yellow
                widget.config(image=self.yellow)
                widget.image = self.yellow
                l = tk.Label(self.frame, image=self.yellow)
                l.place(anchor=tk.NW, x=x_window, y=y_window)
            # widget.config(image=color)
            # widget.image = color
            # l = tk.Label(self.frame, image=color)
            # l.place(anchor=tk.NW, x=x_window, y=y_window)



            # l = tk.Label(self.frame, image=color)
            # l.image = color
            # l.place(anchor=tk.NW, x=x_window, y=y_window)


            self.GamePlay.update_board(x_new, y_new)
        # self.GamePlay.make_history(self.x, self.y, self.x2, self.y2)  # Need to make remove_history mechanism
        print(self.GamePlay.get_history())

    def show_score(self):
        player0, player1 = self.GamePlay.count_total_score()
        l = tk.Label(self.frame, text="Yellow\nscore:\n%d" % player0)
        l.config(font=("Courier", 25))
        l.place(anchor=tk.NW, x=XSPACE/4, y=YSPACE + (EDGE_SIZE - 1) * IMG_SPACE /2)
        l = tk.Label(self.frame, text="Blue\nscore:\n%d" % player1)
        l.config(font=("Courier", 25))
        l.place(anchor=tk.NW, x=XSPACE + (EDGE_SIZE) * IMG_SPACE, y=YSPACE + (EDGE_SIZE - 1) * IMG_SPACE / 2)

    def show_gameover(self):
        won_player = self.GamePlay.who_won()
        l = tk.Label(self.frame, text=" GAME OVER! \n"+won_player+" WON")
        l.config(font=("Courier", 40))
        l.place(anchor=tk.NW, x=XSPACE + (EDGE_SIZE - 1)/4 * IMG_SPACE,
                y=YSPACE + (EDGE_SIZE - 1) * IMG_SPACE / 2)

    def on_click(self, event):
        if event.widget.image == self.blank:
            (self.get_coordinates(event.widget))
            print("Turn", self.GamePlay.turn)
            if self.click_num == 1:

                self.x2, self.y2 = self.get_coordinates(event.widget)
                # print('self.x2, self.y2', self.x2, self.y2)
                if self.GamePlay.moving_the_piece_legal(self.x, self.y, self.x2, self.y2):
                    print(self.GamePlay.moving_the_piece_legal(self.x, self.y, self.x2, self.y2))
                    if self.GamePlay.determine_move_type(self.x, self.y, self.x2, self.y2) == 'walk':
                        self.toggle_color(event.widget)
                        self.invade_color(event.widget)
                        self.GamePlay.turn = (self.GamePlay.turn + 1) % 2
                        self.click_num = (self.click_num + 1) % 2
                    elif self.GamePlay.determine_move_type(self.x, self.y, self.x2, self.y2) == 'jump':
                        self.toggle_color(event.widget)
                        self.delete_color(event.widget)
                        self.invade_color(event.widget)
                        self.GamePlay.turn = (self.GamePlay.turn + 1) % 2
                        self.click_num = (self.click_num + 1) % 2
                        # self.board[y2][x2] = self.board[y][x]
                        # self.board[y][x] = -1
                self.GamePlay.show_board()
                self.show_score()
                if self.GamePlay.is_game_complete():
                    print("Game Over!")
                    self.show_gameover()
            return

        # # Doesnt work but detect location and turn
        # if event.widget.image == self.yellow:
        #     # print(self.GamePlay.whose_turn())
        #
        #     if self.GamePlay.turn == 0:
        #         self.toggle_color(event.widget)
        #     # self.toggle_color(event.widget)
        #     self.GamePlay.turn = (self.GamePlay.turn + 1) % 2
        #     return
        # if event.widget.image == self.blue:
        #     # print(self.GamePlay.whose_turn())
        #     if self.GamePlay.turn == 1:
        #         self.toggle_color(event.widget)
        #     # self.toggle_color(event.widget)
        #     self.GamePlay.turn = (self.GamePlay.turn + 1) % 2
        #     return

        # Working version but just switch color
        if event.widget.image == self.yellow:
            if self.click_num == 0:
                self.x, self.y = self.get_coordinates(event.widget)
                # print("self.x, self.y", self.x, self.y)
                print(self.GamePlay.picking_the_piece_legal(self.x, self.y))
                # print(type(self.x))

                if self.GamePlay.picking_the_piece_legal(self.x, self.y):
                    self.click_num = (self.click_num + 1) % 2
                else:
                    print("Illegal")
            # self.toggle_color(event.widget)
            # self.GamePlay.turn = (self.GamePlay.turn + 1) % 2
            return
        if event.widget.image == self.blue:
            if self.click_num == 0:
                self.x, self.y = self.get_coordinates(event.widget)
                # print("self.x, self.y", self.x, self.y)
                print(self.GamePlay.picking_the_piece_legal(self.x, self.y))
                # print(type(self.x))
                if self.GamePlay.picking_the_piece_legal(self.x, self.y):
                    self.click_num = (self.click_num + 1) % 2
                else:
                    print("Illegal")
            # self.toggle_color(event.widget)
            # self.GamePlay.turn = (self.GamePlay.turn + 1) % 2

            return


        # x, y, z = self.get_coordinates(event.widget)
        # print(x, y, z)
        if self.GamePlay.is_game_complete():
            print("Game Over!")
            self.quit()
        print(self.GamePlay.get_history())

        self.GamePlay.turn = (self.GamePlay.turn + 1) % 2


class GameWindow:
    def __init__(self, window):
        self.frame = tk.Frame(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.frame.pack()
        self.GameBoard = GameBoard(self.frame)


if __name__ == '__main__':
    window = tk.Tk()
    window.wm_title("Spot")
    GameWindow(window)
    window.mainloop()



