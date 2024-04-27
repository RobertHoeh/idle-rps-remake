import curses
from definitions import Button, Pos, rps

class MenuAbstract:
    """A base menu class for methods to make making menus in this game easier.
    Contains basic methods which should be inside the main event loop for all
    menus in the game. Note for future me: remember to make a main function
    that takes the return parameters for all classes and directs them to the
    next class, stores global variables, and calls curses.wrapper() inside it.
    """

    def __init__(
        self,
        buttons: list[list[Button]],
        cursor_pos: Pos = Pos(0, 0)
    ):
        self.buttons: list[list[Button]] = buttons
        self.cursor_pos: Pos = cursor_pos

    def Input(self, w):
        match w.getch():
            case curses.KEY_UP\
            if self.cursor_pos.y != 0:
                self.cursor_pos.y -= 1
            case curses.KEY_DOWN\
            if self.cursor_pos.y != len(self.buttons) - 1:
                self.cursor_pos.y += 1
            case curses.KEY_RIGHT\
            if self.cursor_pos.x != len(self.buttons[0]) - 1:
                self.cursor_pos.x += 1
            case curses.KEY_LEFT\
            if self.cursor_pos.x != 0:
                self.cursor_pos.x -= 1
            case 10: #10 = KEY_ENTER. For some reason curses.KEY_ENTER doesn't work
                button = self.buttons[self.cursor_pos.y][self.cursor_pos.x]
                return button.action
        return None

    def write_buffer(self, w):
        for p1, _ in enumerate(self.buttons):
            for p2, button in enumerate(_):
                if [p1, p2] == [self.cursor_pos.y, self.cursor_pos.x]:
                    w.addstr(button.pos.y,
                                button.pos.x,
                                button.text,
                                curses.A_REVERSE)
                else:
                    w.addstr(button.pos.y,
                                button.pos.x,
                                button.text)
        
        w.refresh()
