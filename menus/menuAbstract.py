import curses

class MenuAbstract:
    """A base menu class for methods to make making menus in this game easier.
    Contains basic methods which should be inside the main event loop for all
    menus in the game. Note for future me: remember to make a main function
    that takes the return parameters for all classes and directs them to the
    next class, stores global variables, and calls curses.wrapper() inside it.
    """

    def __init__(self, menu_items, menu_pos):
        self.menu_items = menu_items
        self.menu_pos = menu_pos
        self.cursor_pos = [0, 0]

    def Input(self, w):
        match w.getch():
            case 259:
                self.cursor_pos[0] -= 1
            case 258:
                self.cursor_pos[0] += 1
            case 261:
                self.cursor_pos[1] += 1
            case 260:
                self.cursor_pos[1] -= 1
            case 10:
                return self.process_input(w)
        return None

    def write_buffer(self, w):
        for p1, i in enumerate(self.menu_items):
            for p2, v in enumerate(i):
                if self.menu_items[self.cursor_pos[0] % len(self.menu_items)]\
                        [self.cursor_pos[1] % len(i)] == v:
                    w.addstr(self.menu_pos[p1][p2][0],
                             self.menu_pos[p1][p2][1],
                             v,
                             curses.A_REVERSE)
                else:
                    w.addstr(self.menu_pos[p1][p1][0],
                             self.menu_pos[p1][p2][1],
                             v)
        w.refresh()

    def process_input(self, w):
        act = self.menu_items[self.cursor_pos[0]][self.cursor_pos[1]]
        return ["rock", "paper", "scissors", "shop", "End Screen", "exit", "start"].index(act)
