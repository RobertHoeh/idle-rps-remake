from enum import Enum
from dataclasses import dataclass

class rps(Enum):
    rock = 0
    paper = 1
    scissors = 2
    shop = 3
    end = 4
    save = 5
    home = 6

class status(Enum):
    win = 1
    loss = 2
    invalid = -1
    tie = 3

@dataclass
class item:
    name: string
    price: tuple[int, int, int]
    description: string
    bonus: tuple[string, float]

items = [
    item("quarry", (5, 0, 0), "Increases rock production by 50%", (r"%rock", 0.5)),
    item("forest", (0, 5, 0), "Increases paper production by 50%", (r"%paper", 0.5)),
    item("sharp blades", (0, 0, 5), "Increases scissors production by 50%", (r"%scissors", 0.5)),
    item("catapult", (10, 10, 10), "Increases all production by 10%", (r"%scissors", 0.1)),
    item("Autoclicker", (30, 30, 30), "Doubles offline production", (r"%CUSTOM", 0)),
    item("Always on", (60, 60, 60), "Doubles offline production again", (r"%CUSTOM", 0)),
    item("End Screen", (1000, 1000, 1000), "Gives you an end screen", (r"%CUSTOM", 0))
]