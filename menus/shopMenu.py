import curses
from menuAbstract import MenuAbstract
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
        name = item.name
        price = item.price
        description = item.description
        description += " "*(241-len(description))
        w.addstr(0, 0, prep_details_str(item))
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
