from menuAbstract import MenuAbstract
import curses
from graphics import graphics_list
from graphics import main_menu_text
from definitions import rps
from definitions import status

class home_menu(MenuAbstract):
    def __init__(self, last_move, resources, show_end_scr):
        """last_move is a two element list of the last moves done.
        -1 = reserved value, first move/ tutorial
        0 = rock
        1 = paper
        2 = scissors"""
        menu_items = (("rock", "paper", "scissors"), ("shop", "End Screen", "exit"))
        menu_pos = (((11, 5), (11, 19), (11, 32)), ((13, 5), (13, 17), (13, 34)))
        super().__init__(menu_items, menu_pos)
        self.last_move = last_move
        self.money = 0
        self.resources = resources
        self.show_end_scr = show_end_scr
    def main(self):
        curses.wrapper(self.home)

    def reversed(self, var):
        return "".join(["(" if i == ")" else
                        ")" if i == "(" else
                        i for i in var[::-1]])

    def home(self, w):
        win_text = lambda b:\
            f"{' '*41}" if b == -1 else\
            f"{' '*15}Player Won!{' '*15}" if b == 1 else\
            f"{' '*17}AI Won!{' '*17}" if b == 2 else\
            f"{' '*15}Nobody Won!{' '*15}"
        curses.curs_set(0)
        w.clear()
        w.addstr(0, 0, main_menu_text(
            win_text(self.game_logic(self.last_move, True)),
            self.resources))
        
        if self.last_move[0] < 3 or self.last_move[1] < 3:
            player_graphic = graphics_list[self.last_move[0]].splitlines()
            ai_graphic = graphics_list[self.last_move[1]].splitlines()
            for i in range(6):
                w.addstr(i+1, 1, player_graphic[i])
                w.addstr(i+1, 24, self.reversed(ai_graphic[i])
        if self.show_end_scr:
            w.addstr(19, 0, "You have not yet unlocked the end screen!")
        while True:
            try:
                # get input and change cursor_pos correspondingly
                rcode = super().Input(w)
                if rcode != None:
                    return rcode

                # write buffer: includes graphical renditions.
                super().write_buffer(w)
            except IndexError:
                while True:
                    w.clear()
                    w.addstr(0, 0, "wait, that's illegal")

    def game_logic(self, input, ig_ran):
        """If ig_ran = true, ingores random and takes a two integer list entry
        If not, generates a random number for ai_input"""
        ai_input = input[1]
        input = input[0]
        
        if ai_input == rps.rock and input == rps.paper or\
        ai_input == rps.paper and input == rps.scissors or\
        ai_input == rps.scissors and input == rps.rock:
            return status.win
        elif input == rps.rock and ai_input == rps.paper or\
        input == rps.paper and ai_input == rps.scissors or\
        input == rps.scissors and ai_input == rps.rock:
            return status.loss
        elif input == -1:
            return status.invalid
        else:
            return status.tie
