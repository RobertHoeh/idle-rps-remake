import curses
from menuAbstract import MenuAbstract
from definitions import rps
from graphics import base_str
from graphics import prep_items_str
from graphics import prep_submenu_text
from graphics import prep_details_str

class shop_menu(MenuAbstract):
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
        self.items_str = prep_items_str(items_avail)
        self.code = False
        
    def menu_str(self, w, pos):
        for p, i in enumerate(self.items_str.splitlines()[pos * 3:(pos * 3) + 9]):
            w.addstr(4+p, 0, i)

    def Input(self, w):
        bounds = len(self.items_avail)
        outside = bounds != 0
        if not outside:
            self.cursor_pos = -1
        else:
            match (w.getch(), outside):
                case (258, True) if self.cursor_pos <= bounds - 2:
                    self.cursor_pos += 1
                case (259, True) if self.cursor_pos >= 0:
                    self.cursor_pos -= 1
                case (10, False):
                    self.code = True
                case (10, True):
                    self.submenu = not self.submenu
                    self.last_pos = self.cursor_pos
                    self.cursor_pos = 0
                    w.addstr(0, 0, base_str)
    
    def main(self):
        curses.wrapper(self.shop_menu)

    def render_selection(self, w):
        try:
            w.chgat(1, 0, 42, curses.A_NORMAL)
            w.chgat(5, 0, 42, curses.A_NORMAL)
            item = self.items_avail[self.cursor_pos].name
            if self.cursor_pos >= 0:
                self.xpos = len(f"││{' '*(16-(len(item)//2))}")
                w.chgat(5, self.xpos, len(item), curses.A_REVERSE)
            elif self.cursor_pos == -1:
                w.chgat(1, 1, 40, curses.A_REVERSE)
        except IndexError:
            w.chgat(1, 1, 40, curses.A_REVERSE)
            w.chgat(5, 0, 42, curses.A_NORMAL)

    def submenu_input(self, w):
        match w.getch():
            case 258 if self.cursor_pos <= 1:
                self.cursor_pos += 1
                return None
            case 259 if self.cursor_pos >= 1:
                self.cursor_pos -= 1
                return None
            case 10:
                match self.cursor_pos:
                    case 0:
                        return(self.items_avail[self.cursor_pos])
                    case 1:
                        self.details(w)
                    case 2:
                        self.submenu = False
                        self.cursor_pos = self.last_pos
                        w.addstr(0, 0, base_str)
    
    def render_submenu(self, w):
        for p, i in enumerate(prep_submenu_text(self.items_avail[self.last_pos].name)[:-1]):
            w.addstr(4+p, 31, i)
        if self.cursor_pos == 0:
            w.chgat(10, 35, 3, curses.A_REVERSE)
        elif self.cursor_pos == 1:
            w.chgat(11, 33, 7, curses.A_REVERSE)
        elif self.cursor_pos == 2:
            w.chgat(12, 34, 5, curses.A_REVERSE)
            
  
    def shop_menu(self, w):
        w.clear()
        curses.curs_set(0)
        w.addstr(0,0, base_str)
        while True:
            w.addstr(20, 0, str(self.resources))
            if not self.submenu:
                self.menu_str(w, self.cursor_pos)
                self.Input(w)
                if self.code:
                    return rps.home
                self.render_selection(w)
            if self.submenu:
                self.menu_str(w, self.last_pos)
                self.render_submenu(w)
                code = self.submenu_input(w)
                if code != None:
                    return code
            w.refresh()

    def details_str(self, w, item):
        name = item.name
        price = item.price
        description = item.description
        description += " "*(241-len(description))
        w.addstr(0, 0, prep_details_str(item))
        for p, i in enumerate(range(30, 241, 30)):
            w.addstr(p+3, 11, description[i-30,i])

    def details(self, w):
        self.details_str(w, self.items_avail[self.last_pos])
        while True:
            if w.getch() != -1:
                self.shop_menu(w)
                break
