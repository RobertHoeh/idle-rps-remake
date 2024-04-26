import curses
from graphics import start_menu_text
from definitions import rps

class start_menu:
    def __init__(self):
        self.cursor_pos = 0
    def main(self):
        curses.wrapper(self.curses_main)
    def print_str(self, w):
        for p, v in enumerate(start_menu_text):
            w.addstr(p, 0, v)
    def curses_main(self, w):
        curses.curs_set(0)
        self.print_str(w)
        w.chgat(10, 41, 5, curses.A_REVERSE)
        while True:
            char = w.getch()

            if char == 258 and self.cursor_pos <= 1:
                self.cursor_pos += 1
            if char == 259 and self.cursor_pos >= 1:
                self.cursor_pos -= 1
            if char == 10:
                return [rps.home, rps.save][self.cursor_pos]

            # since cursor_pos only has 3 possibilities, this works fine?
            match self.cursor_pos:
                case 0:
                    w.chgat(10, 41, 5, curses.A_REVERSE)
                    w.chgat(11, 41, 5, curses.A_NORMAL)
                    w.chgat(12, 40, 7, curses.A_NORMAL)
                case 1:
                    w.chgat(10, 41, 5, curses.A_NORMAL)
                    w.chgat(11, 41, 5, curses.A_REVERSE)
                    w.chgat(12, 40, 7, curses.A_NORMAL)
                case 2:
                    w.chgat(10, 41, 5, curses.A_NORMAL)
                    w.chgat(11, 41, 5, curses.A_NORMAL)
                    w.chgat(12, 40, 7, curses.A_REVERSE)
            w.refresh()