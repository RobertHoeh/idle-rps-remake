import curses,
       os,
       time,
       math,
       sys
import random as rand
from menus.startMenu import start_menu
from menus.shopMenu import shop_menu
from menus.homeMenu import home_menu
from definitions import rps
from definitions import items
from definitions import game_logic
from definitions import status
from graphics import end_screen


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
            match code:
                case rps.rock:
                    self.last_turn = [0, rand.randint(0,2)]
                    self.resources[0] += game_logic(self.last_turn)*self.increases[0]*self.increases[3] == status.win
                    code = rps.home
                case rps.paper:
                    self.last_turn = [1, rand.randint(0,2)]
                    self.resources[1] += game_logic(self.last_turn)*self.increases[1]*self.increases[3] == status.win
                    code = rps.home
                case rps.scissors:
                    self.last_turn = [2, rand.randint(0,2)]
                    self.resources[2] += game_logic(self.last_turn)*self.increases[2]*self.increases[3] == status.win
                    code = rps.home
                case rps.shop:
                    menu = shop_menu(self.resources, items)
                    code = menu.shop_menu(w)
                case rps.end:
                    if self.end_scr:
                        self.display_end_screen(w)
                        code = rps.home
                    else:
                        show_end_scr = True
                        code = rps.home
                case rps.save:
                    self.write_save()
                    sys.exit()
                case rps.home:
                    menu = home_menu(self.last_turn, self.resources, show_end_scr)
                    code = menu.home(w)
                    self.show_end_scr = False
                case _:
                    self.buy(code, False)
                    code = rps.shop

    def buy(self, item, BYPASS):
        type = item.bonus[0]
        inc = item.bonus[1]
        resources = item.resources
        avail = all([x>=y for x, y in zip(self.resources, resources)])
        if avail or BYPASS:
            if type != r"%CUSTOM":
                self.increases[[r"%rock", r"%paper", r"%scissors", r"%all"].index(type)] += inc
            else:
                self.custom(item)
            items = [x for x in items if x != item]
            # https://chat.openai.com/chat/6631c5c7-fc61-4cb2-bc2c-5fb087c8ddd1
            self.resources = [x-y for x, y in zip(self.resources, resources)]
            self.items_purchased.append(item)

    def custom(self, item):
        if item.name == "Autoclicker" or item.name == "Always on":
            self.rate *= 2
        if item.name == "End Screen":
            self.end_scr = True

    def display_end_screen(self, w):
        w.clear()
        char = -1
        graphics = end_screen
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


    """TODO: implement JSON saving"""
    def write_save(self):
        if not os.path.exists(f"{self.get_game_dir()}/game_save.txt"):
            self.create_save()
        match sys.plaform:
            case 'linux':
                f = open(f"{self.get_game_dir()}/game_save.txt", "r+")
            case 'nt':
                f = open(f"{self.get_game_dir()}\\game_save.txt", "r+")
            case _:
                raise Exception("Unsupported platform!")

        f.write(f"{time.time()}\n{self.resources[rps.rock]}\n{self.resources[rps.paper]}\n{self.resources[rps.scissors]}\n{self.rate}\n{"\n".join([i.name for i in self.items_purchased])}")
        f.close()

    def read_save(self):
        if os.path.exists(f"{self.get_game_dir()}/game_save.txt"):
            match sys.platform:
                case 'linux':
                    f = open(f"{self.get_game_dir()}/game_save.txt", "r")
                case 'nt':
                    f = open(f"{self.get_game_dir()}\\game_save.txt", "r")
                case _:
                    raise Exception("Unsupported platform!")

        save = f.readlines()
        f.close()
        self.rate = float(save[4])
        for i in items:
            if save.count(i.name) != 0:
                self.buy(i, True)
        deltat = math.floor(time.time() - float(save[0]))
        self.resources = [math.ceil(float(save[1]) + ((self.increases[0] + self.increases[3]) * deltat * self.rate * (2/9))),
                          math.ceil(float(save[2]) + ((self.increases[1] + self.increases[3]) * deltat * self.rate * (2/9))),
                          math.ceil(float(save[3]) + ((self.increases[2] + self.increases[3]) * deltat * self.rate * (2/9)))]
        # ^ I know this is generally a bad idea, but it should work fine in this case
