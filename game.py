import curses
import os
import time
import math
import random as rand
import sys
from menus.startMenu import start_menu
from menus.shopMenu import shop_menu
from menus.homeMenu import home_menu
from definitions import rps


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
            if code == rps.rock:
                self.last_turn = [0, rand.randint(0,2)]
                self.resources[0] += self.game_logic(self.last_turn)*self.increases[0]*self.increases[3]
                code = 6
            elif code == rps.paper:
                self.last_turn = [1, rand.randint(0,2)]
                self.resources[1] += self.game_logic(self.last_turn)*self.increases[1]*self.increases[3]
                code = 6
            elif code == rps.scissors:
                self.last_turn = [2, rand.randint(0,2)]
                self.resources[2] += self.game_logic(self.last_turn)*self.increases[2]*self.increases[3]
                code = 6
            elif code == rps.shop:
                menu = shop_menu(self.resources, self.items)
                code = menu.shop_menu(w)
            elif code == rps.end:
                if self.end_scr:
                    self.end_screen(w)
                    code = 6
                else:
                    show_end_scr = True
                    code = 6
            elif code == rps.save:
                self.write_save()
                sys.exit()
            elif code == rps.home:
                menu = home_menu(self.last_turn, self.resources, show_end_scr)
                code = menu.home(w)
                self.show_end_scr = False
            else:
                self.buy(code, False)
                code = rps.shop

    def game_logic(self, input):
        """If ig_ran = true, ingores random and takes a two integer list entry
        If not, generates a random number for ai_input
        0 = rock
        1 = paper
        2 = scissors"""
        ai_input = input[1]
        input = input[0]
        
        if ai_input == rps.rock and input == rps.paper or\
        ai_input == rps.paper and input == rps.scissors or\
        ai_input == rps.scissors and input == rps.rock:
            return True
        elif input == rps.rock and ai_input == rps.paper or\
        input == rps.paper and ai_input == rps.scissors or\
        input == rps.scissors and ai_input == rps.rock:
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

        f.write(f"{time.time()}\n{self.resources[rps.rock]}\n{self.resources[rps.paper]}\n{self.resources[rps.scissors]}\n{self.rate}\n{nl.join([i[0] for i in self.items_purchased])}")
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
