import curses

class start_menu:
    def __init__(self):
        self.cursor_pos = 0
        self.string = [r"┌─────────────────────────────────────────────────────────────────────────────────────┐",
r"│ ___   ________   ___        _______           ________   ________   ________        │",
r"│ |\  \ |\   ___ \ |\  \      |\  ___ \         |\   __  \ |\   __  \ |\   ____\      │",
r"│ \ \  \\ \  \_|\ \\ \  \     \ \   __/|        \ \  \|\  \\ \  \|\  \\ \  \___|_     │",
r"│  \ \  \\ \  \ \\ \\ \  \     \ \  \_|/__       \ \   _  _\\ \   ____\\ \_____  \    │",
r"│   \ \  \\ \  \_\\ \\ \  \____ \ \  \_|\ \       \ \  \\  \|\ \  \___| \|____|\  \   │",
r"│    \ \__\\ \_______\\ \_______\\ \_______\       \ \__\\ _\ \ \__\      ____\_\  \  │",
r"│     \|__| \|_______| \|_______| \|_______|        \|__|\|__| \|__|     |\_________\ │",
r"│                                                                        \|_________| │",
r"├─────────────────────────────────────────────────────────────────────────────────────┤",
r"│                                        start                                        │",
r"│                                        close                                        │",
r"└─────────────────────────────────────────────────────────────────────────────────────┘"]
    def main(self):
        curses.wrapper(self.curses_main)
    def print_str(self, w):
        for p, v in enumerate(self.string):
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
                if self.cursor_pos == 0:
                    return 6
                if self.cursor_pos == 1:
                    return 5

            # since cursor_pos only has 3 possibilities, this works fine?
            if self.cursor_pos == 0:
                w.chgat(10, 41, 5, curses.A_REVERSE)
                w.chgat(11, 41, 5, curses.A_NORMAL)
                w.chgat(12, 40, 7, curses.A_NORMAL)
            if self.cursor_pos == 1:
                w.chgat(10, 41, 5, curses.A_NORMAL)
                w.chgat(11, 41, 5, curses.A_REVERSE)
                w.chgat(12, 40, 7, curses.A_NORMAL)
            if self.cursor_pos == 2:
                w.chgat(10, 41, 5, curses.A_NORMAL)
                w.chgat(11, 41, 5, curses.A_NORMAL)
                w.chgat(12, 40, 7, curses.A_REVERSE)
            w.refresh()