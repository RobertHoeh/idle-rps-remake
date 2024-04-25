from menuAbstract import MenuAbstract
import curses

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
