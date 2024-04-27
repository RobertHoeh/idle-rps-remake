import curses
from definitions import Button, Pos, rps

class MenuAbstract:
    """A base menu class for methods to make making menus in this game easier.
    Contains basic methods which should be inside the main event loop for all
    menus in the game. Note for future me: remember to make a main function
    that takes the return parameters for all classes and directs them to the
    next class, stores global variables, and calls curses.wrapper() inside it.
    """

    def __init__(self, buttons: list[list[Button]]):
        self.buttons: list[list[Button]] = buttons
        self.cursor_pos: Pos = Pos(0, 0)

    def Input(self, w):
        match w.getch():
            case curses.KEY_UP:
                self.cursor_pos.y -= 1
            case curses.KEY_DOWN:
                self.cursor_pos.y += 1
            case curses.KEY_RIGHT:
                self.cursor_pos.x += 1
            case curses.KEY_LEFT:
                self.cursor_pos.x -= 1
            case curses.KEY_ENTER:
                return self.process_input(w)
        return None

    def write_buffer(self, w):
        for p1, _ in enumerate(self.buttons):
            for p2, button in enumerate(_):
                w.addstr(button.pos.y
                            button.pos.x,
                            button.text,
                            curses.A_REVERSE
                            if button.pos == self.cursor_pos
                            else curses.A_NORMAL)
        w.refresh()

    def process_input(self, w):
        button = self.buttons[self.cursor_pos.y][self.cursor_pos.x]
        return button.action
