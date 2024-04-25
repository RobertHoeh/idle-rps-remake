import curses
import sys
import random as rand
import numpy as np
import os
import time
import math

"""-------------------------IMPORTANT INFORMATION-------------------------
   |Idk why I'm making this so fancy, but all of the xxxx.main() classes |
   |in the objects are just for testing. They won't be used in the final |
   |code, because the wrapper class will simply use curses.wrapper() and |
   |pass the w parameter to the classes.                                 |
   -----------------------------------------------------------------------"""

class menu_base:
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
        uin = w.getch()
        if uin == 259:
            self.cursor_pos[0] -= 1
            return None

        elif uin == 258:
            self.cursor_pos[0] += 1
            return None

        elif uin == 261:
            self.cursor_pos[1] += 1
            return None

        elif uin == 260:
            self.cursor_pos[1] -= 1
            return None

        elif uin == 10:
            return self.process_input(w)

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
        

class home_menu(menu_base):

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
        self.graphics_list = ["""\
    _______  
---'   ____) 
      (_____)
      (_____)
      (____) 
---.__(___)  
""",
                          """\
     _______      
---'    ____)____ 
           ______)
          _______)
         _______) 
---.__________)   
""",
                          """\
    _______       
---'   ____)____  
          ______) 
       __________)
      (____)      
---.__(___)       
"""]

    def main(self):
        curses.wrapper(self.home)

    def reverse_parenthesis(self, var):
        return "".join(["(" if i == ")" else
                        ")" if i == "(" else
                        i for i in var])

    def home(self, w):
        a = lambda b:\
            f"{' '*41}" if b == -1 else\
            f"{' '*15}Player Won!{' '*15}" if b == 1 else\
            f"{' '*17}AI Won!{' '*17}" if b == 2 else\
            f"{' '*15}Nobody Won!{' '*15}"
        curses.curs_set(0)
        w.clear()
        w.addstr(0, 0,
                  "┌────────────────────┬────────────────────┐\n"+
                  "│                    │                    │\n"*7+
                  "├────────────────────┴────────────────────┤\n"+
                 f"│{a(self.game_logic(self.last_move, True))}│\n"+
                  "├────────────┬───────────────┬────────────┤\n"+
                  "│    rock    │     paper     │  scissors  │\n"+
                  "├────────────┼───────────────┼────────────┤\n"+
                  "│    shop    │   End Screen  │    exit    │\n"+
                  "├────────────┼───────────────┼────────────┤\n"+
                  "│    rock    │     paper     │  scissors  │\n"+
                 f"│{str(self.resources[0]).center(12)}│{str(self.resources[1]).center(15)}│{str(self.resources[2]).center(12)}│\n"+
                  "└────────────┴───────────────┴────────────┘")
        if self.last_move[0] in range(len(self.graphics_list)) or\
        self.last_move[1] in range(len(self.graphics_list)):
            player_graphic = self.graphics_list[self.last_move[0]].splitlines()
            ai_graphic = self.graphics_list[self.last_move[1]].splitlines()
            for i in range(6):
                player_graphic_line = player_graphic[i]
                ai_graphic_line = ai_graphic[i][::-1]
                w.addstr(i+1, 1, player_graphic_line)
                w.addstr(i+1, 24, self.reverse_parenthesis(ai_graphic_line))
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
        
        if ai_input == 0 and input == 1 or\
        ai_input == 1 and input == 2 or\
        ai_input == 2 and input == 0:
            return 1
        elif input == 0 and ai_input == 1 or\
        input == 1 and ai_input == 2 or\
        input == 2 and ai_input == 0:
            return 2
        elif input == -1:
            return -1
        else:
            return 3

class shop_menu(menu_base):
    def __init__(self, resources, items_avail):
        """resources is a dict of the resources available to the player as
        well as their amounts. items_avail is a list of the items available
        to the player in the shop (eventually will make into a list of items as 
        a tuple including their name, a tuple for resources needed, and the
        item's description. Item names cannot be more than 27 characters long, 
        however the recommended limit is 9 characters. Everything past that 
        starts getting kinda weird."""
        
        self.resources = resources
        self.items_avail = items_avail
        self.cursor_pos = 0
        self.submenu = False
        self.base_str = """┌────────────────────────────────────────┐
│                  quit                  │
└────────────────────────────────────────┘
┌──────────────────────────────┬─────────┐
│                              │         │
│                              │         │
│                              │         │
│                              │         │
│                              │         │
│                              │         │
│                              │         │
│                              │         │
│                              │         │
└──────────────────────────────┴─────────┘"""
        try:
            self.items_str = "".join([f"│┌────────────────────────────┐│\n││{' '*(14-(len(item[0])//2))}{item[0]}{' '*(14-(len(item[0])//2)-(len(item[0])%2))}││\n│└────────────────────────────┘│\n" for item in items_avail])
        except:
            raise Exception("pause here pwease")
        self.items_str += "│                              │\n"*10
        self.code = False
        
    def menu_str(self, w, pos):
        for p, i in enumerate(self.items_str.splitlines()[pos * 3:(pos * 3) + 9]):
            w.addstr(4+p, 0, i)

    def Input(self, w):
        char = w.getch()
        if char == 258 and self.cursor_pos <= len(self.items_avail) - 2 and len(self.items_avail) != 0:
            self.cursor_pos += 1
        
        if char == 259 and self.cursor_pos >= 0 and len(self.items_avail) != 0:
            self.cursor_pos -= 1
        
        if len(self.items_avail) == 0:
            self.cursor_pos = -1
        if char == 10:
            if self.cursor_pos == -1:
                self.code = True
            else:
                self.submenu = not self.submenu
                self.last_pos = self.cursor_pos
                self.cursor_pos = 0
                w.addstr(0, 0, self.base_str)
    
    def main(self):
        curses.wrapper(self.shop_menu)

    def render_selection(self, w):
        try:
            w.chgat(1, 0, 42, curses.A_NORMAL)
            w.chgat(5, 0, 42, curses.A_NORMAL)
            item = self.items_avail[self.cursor_pos][0]
            if self.cursor_pos >= 0:
                self.xpos = len(f"││{' '*(16-(len(item)//2))}")
                w.chgat(5, self.xpos, len(item), curses.A_REVERSE)
            elif self.cursor_pos == -1:
                w.chgat(1, 1, 40, curses.A_REVERSE)
        except IndexError:
            w.chgat(1, 1, 40, curses.A_REVERSE)
            w.chgat(5, 0, 42, curses.A_NORMAL)


#    def render_selection(self, w):
#        # Highlight the quit button
#        if self.cursor_pos == -1:
#            w.chgat(1, 1, 40, curses.A_REVERSE)
#        else:
#            w.chgat(1, 0, 42, curses.A_NORMAL)
#            
#        # Highlight the selected menu item
#        # Menu items don't highlight (I think replit's fault). Will fix later
#        if self.cursor_pos >= 0:
#            x_pos = 3 + 13 - (len(self.items_avail[self.cursor_pos][0]) // 2)
#            w.chgat(5, x_pos, len(self.items_avail[self.cursor_pos][0]), curses.A_REVERSE)
#        else:
#            w.chgat(5, 0, 42, curses.A_NORMAL)

    def submenu_input(self, w):
        char = w.getch()
        if char == 258 and self.cursor_pos <= 1:
            self.cursor_pos += 1
            return None
        if char == 259 and self.cursor_pos >= 1:
            self.cursor_pos -= 1
            return None
        if char == 10:
            if self.cursor_pos == 0:
                return(self.items_avail[self.cursor_pos])
            if self.cursor_pos == 1:
                self.details(w)
            if self.cursor_pos == 2:
                self.submenu = False
                self.cursor_pos = self.last_pos
                w.addstr(0, 0, self.base_str)
    
    def render_submenu(self, w):
        for p, i in enumerate(self.prep_submenu_text(w)[:-1]):
            w.addstr(4+p, 31, i)
        if self.cursor_pos == 0:
            w.chgat(10, 35, 3, curses.A_REVERSE)
        elif self.cursor_pos == 1:
            w.chgat(11, 33, 7, curses.A_REVERSE)
        elif self.cursor_pos == 2:
            w.chgat(12, 34, 5, curses.A_REVERSE)
            
    
    def prep_submenu_text(self, w):
        # Returns a list of strings to print for each row bc that's how curses 
        # works
        name = self.items_avail[self.last_pos][0]
        if len(name) == 0:
            raise Exception("You can't do that")
        if len(name) in range(10):
            return [f"│{' '*(4-len(name)//2)}{name}{' '*(5-len(name)//2-(len(name)%2))}│",
                    "│         │",
                    "│         │",
                    "│         │",
                    "│         │",
                    "├─────────┤",
                    "│   buy   │",
                    "│ details │",
                    "│  close  │",
                   0]
        elif len(name) in range(10, 19):
            return [f"│{name[0:9]}│",
                    f"│{' '*(4-len(name[9:19])//2)}{name[9:19]}{' '*(5-len(name[9:19])//2-(len(name[9:19])%2))}│",
                    "│         │",
                    "│         │",
                    "│         │",
                    "├─────────┤",
                    "│   buy   │",
                    "│ details │",
                    "│  close  │",
                   1]
        elif len(name) in range(19, 28):
            return [f"│{name[0:9]}│",
                    f"│{name[9:19]}│"
                    f"│{' '*(4-len(name[19:28])//2)}{name[19:28]}{' '*(5-len(name[19:28])//2-(len(name[19:28])%2))}│",
                    "│         │",
                    "│         │",
                    "├─────────┤",
                    "│   buy   │",
                    "│ details │",
                    "│  close  │",
                   0]
        else:
            raise Exception("You can't do that")
            
  
    def shop_menu(self, w):
        w.clear()
        curses.curs_set(0)
        w.addstr(0,0, self.base_str)
        while True:
            w.addstr(20, 0, str(self.resources))
            if not self.submenu:
                self.menu_str(w, self.cursor_pos)
                self.Input(w)
                if self.code:
                    return 6
                self.render_selection(w)
            if self.submenu:
                self.menu_str(w, self.last_pos)
                self.render_submenu(w)
                code = self.submenu_input(w)
                if code != None:
                    return code
            w.refresh()

    def details_str(self, w, item):
        name = item[0]
        resources = item[1]
        description = item[2]
        description += " "*(241-len(description))
        w.addstr(0, 0, "┌────────────────────────────────────────┐\n"
               f"│{name.center(40)}│\n"
                "├─────────┬──────────────────────────────┤\n"
               f"│rock:    │                              │\n"
               f"│{resources[0]}{' '*(9-len(str(resources[0])))}│                              │\n"
               f"│paper:   │                              │\n"
               f"│{resources[1]}{' '*(9-len(str(resources[1])))}│                              │\n"
               f"│scissors:│                              │\n"
               f"│{resources[2]}{' '*(9-len(str(resources[2])))}│                              │\n"
               f"│         │                              │\n"
               f"│         │                              │\n"
                "├─────────┴──────────────────────────────┤\n"
                "│         Press any key to exit.         │\n"
                "└────────────────────────────────────────┘\n")
        w.addstr(3, 11, description[0:30])
        w.addstr(4, 11, description[30:60])
        w.addstr(5, 11, description[60:90])
        w.addstr(6, 11, description[90:120])
        w.addstr(7, 11, description[120:150])
        w.addstr(8, 11, description[150:180])
        w.addstr(9, 11, description[180:210])
        w.addstr(10, 11, description[210:240])
    def details(self, w):
        self.details_str(w, self.items_avail[self.last_pos])
        while True:
            if w.getch() != -1:
                self.shop_menu(w)
                break

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

class game:
    """
    ------------------------------ITEM DOCUMENTATION------------------------------
    |first entry includes name, second includes price (in rock, paper, scissors),|
    | third includes description, and fifth includes boosts (in %rock, %paper, %s|
    |cissors, %all, or CUSTOM). Custom is reserved and cannot be used for anythin|
    |g that isn't directly implemented. Due to how python strings work, use raw s|
    |trings for these. Use decimals (or fractions) for the percent values.       |
    ------------------------------------------------------------------------------"""
    def __init__(self):
        self.items = [("quarry", (5, 0, 0), "Increases rock production by 50%", (r"%rock", 0.5)),
                       ("forest", (0, 5, 0), "Increases paper production by 50%", (r"%paper", 0.5)),
                       ("sharp blades", (0, 0, 5), "Increases scissors production by 50%", (r"%scissors", 0.5)),
                       ("catapult", (10, 10, 10), "Increases all production by 10%", (r"%scissors", 0.1)),
                       ("Autoclicker", (30, 30, 30), "Doubles offline production", (r"%CUSTOM", 0)),
                       ("Always on", (60, 60, 60), "Doubles offline production again", (r"%CUSTOM", 0)),
                       ("End Screen", (1000, 1000, 1000), "Gives you an end screen", (r"%CUSTOM", 0))]
        self.items_purchased = []
        self.last_turn = [-1, -1]
        self.increases = [1, 1, 1, 1]
        self.resources = [0, 0, 0]
        self.rate = 0.1
        self.end_scr = False
        self.show_end_scr = False

    def main(self):
        curses.wrapper(self.main_curses)

    def main_curses(self, w):
        if not os.path.exists(f"{self.get_game_dir()}/game_save.txt"):
            self.create_save()
        if os.path.exists(f"{self.get_game_dir()}/game_save.txt"):
            self.read_save()
        menu = start_menu()
        code = menu.curses_main(w)
        show_end_scr = False
        while True:
            if code == 0:
                self.last_turn = [0, rand.randint(0,2)]
                self.resources[0] += self.game_logic(self.last_turn)*self.increases[0]*self.increases[3]
                code = 6
            elif code == 1:
                self.last_turn = [1, rand.randint(0,2)]
                self.resources[1] += self.game_logic(self.last_turn)*self.increases[1]*self.increases[3]
                code = 6
            elif code == 2:
                self.last_turn = [2, rand.randint(0,2)]
                self.resources[2] += self.game_logic(self.last_turn)*self.increases[2]*self.increases[3]
                code = 6
            elif code == 3:
                menu = shop_menu(self.resources, self.items)
                code = menu.shop_menu(w)
            elif code == 4:
                if self.end_scr:
                    self.end_screen(w)
                    code = 6
                else:
                    show_end_scr = True
                    code = 6
            elif code == 5:
                self.write_save()
                sys.exit()
            elif code == 6:
                menu = home_menu(self.last_turn, self.resources, show_end_scr)
                code = menu.home(w)
                self.show_end_scr = False
            else:
                self.buy(code, False)
                code = 3

    def game_logic(self, input):
        """If ig_ran = true, ingores random and takes a two integer list entry
        If not, generates a random number for ai_input
        0 = rock
        1 = paper
        2 = scissors"""
        ai_input = input[1]
        input = input[0]
        
        if ai_input == 0 and input == 1 or\
        ai_input == 1 and input == 2 or\
        ai_input == 2 and input == 0:
            return True
        elif input == 0 and ai_input == 1 or\
        input == 1 and ai_input == 2 or\
        input == 2 and ai_input == 0:
            return False
        elif input == ai_input:
            return True
        else:
            raise Exception("unexpected game_logic value.")

    def buy(self, item, BYPASS):
        type = item[3][0]
        inc = item[3][1]
        resources = item[1]
        avail = all([x>=y for x, y in zip(self.resources, resources)])
        if avail or BYPASS:
            if type != r"CUSTOM":
                self.increases[[r"%rock", r"%paper", r"%scissors", r"%all"].index(type)] += inc
            else:
                self.custom(item)
            self.items = [x for x in self.items if x != item]
            # https://chat.openai.com/chat/6631c5c7-fc61-4cb2-bc2c-5fb087c8ddd1
            self.resources = [x-y for x, y in zip(self.resources, resources)]
            self.items_purchased.append(item)

    def custom(self, item):
        if item[0] == "Autoclicker" or item[0] == "Always on":
            self.rate *= 2
        if item[0] == "End Screen":
            self.end_scr = True

    def prep_end_screen(self):
        graphics_list = ["""\
│    _______   │       _______    │
│---'   ____)  │ ____(____    '---│
│      (_____) │(______           │
│      (_____) │(_______          │
│      (____)  │ (_______         │
│---.__(___)   │   (__________.---│
├──────────────┴──────────────────┤
""",
                          """\
│           _______               │
│       ---'   ____)____          │
│                 ______)         │
│              __________)        │
│             (____)              │
│       ---.__(___)               │
"""]
        return(["┌──────────────┬──────────────────┐"]+
               graphics_list[0].splitlines()+
               graphics_list[1].splitlines()+
               ["├─────────────────────────────────┤",
               "│So, what exactly is this screen  │",
               "│that you just unlocked? Nothing  │",
               "│really, just a generic endscreen │",
               "│and just so happens to be a      │",
               "│citation page for the rock paper │",
               "│ascii art ;)                     │",
               "├─────────────────────────────────┤",
               "│https://gist.github.com/wynand100│",
               "│4/b5c521ea8392e9c6bfe101b025c39ab│",
               "│e                                │",
               "├─────────────────────────────────┤",
               "│      PRESS ANY KEY TO EXIT      │",
               "└─────────────────────────────────┘"])

    def end_screen(self, w):
        w.clear()
        char = -1
        graphics = self.prep_end_screen()
        for p, i in enumerate(graphics):
            w.addstr(p, 0, i)
        while char == -1:
            char = w.getch()

    def get_game_dir(self):
        return os.path.dirname(os.path.abspath(__file__))
        # https://www.delftstack.com/howto/python/python-get-path/#use-the-os-module-to-get-the-path-of-files-and-the-current-working-directory

    def create_save(self):
        if sys.platform == 'linux':
            f = open(f"{self.get_game_dir()}/game_save.txt", "a")
            f.close()

        elif sys.platform == 'nt':
            f = open(f"{self.get_game_dir()}\\game_save.txt", "a")
            f.close()

        else:
            raise Exception("Unsupported platform!")

    def write_save(self):
        nl = "\n"
        if not os.path.exists(f"{self.get_game_dir()}/game_save.txt"):
            # https://www.pythontutorial.net/python-basics/python-check-if-file-exists/
            self.create_save()
        
        if sys.platform == 'linux':
            f = open(f"{self.get_game_dir()}/game_save.txt", "r+")
        
        elif sys.platform == 'nt':
            f = open(f"{self.get_game_dir()}\\game_save.txt", "r+")
        
        else:
            raise Exception("Unsupported platform!")

        
        # https://stackoverflow.com/questions/8220108/how-do-i-check-the-operating-system-in-python
        # ^ used for most platform checking

        f.write(f"{time.time()}\n{self.resources[0]}\n{self.resources[1]}\n{self.resources[2]}\n{self.rate}\n{nl.join([i[0] for i in self.items_purchased])}")
        f.close()

    def read_save(self):
        if os.path.exists(f"{self.get_game_dir()}/game_save.txt"):
            if sys.platform == 'linux':
                f = open(f"{self.get_game_dir()}/game_save.txt", "r")

            elif sys.platform == 'nt':
                f = open(f"{self.get_game_dir()}\\game_save.txt", "r")

            else:
                raise Exception("Unsupported platform!")

        save = f.readlines()
        self.rate = float(save[4])
        for i in self.items:
            if save.count(i[0]) != 0:
                self.buy(i, True)
        deltat = math.floor(time.time() - float(save[0]))
        self.resources = [math.ceil(float(save[1]) + ((self.increases[0] + self.increases[3]) * deltat * self.rate * (2/9))),
                          math.ceil(float(save[2]) + ((self.increases[1] + self.increases[3]) * deltat * self.rate * (2/9))),
                          math.ceil(float(save[3]) + ((self.increases[2] + self.increases[3]) * deltat * self.rate * (2/9)))]
        # ^ I know this is generally a bad idea, but it should work fine in this case

#menu = start_menu()
menu = game()
menu.main()