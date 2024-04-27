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
    name: str
    price: tuple[int, int, int]
    description: str
    bonus: tuple[str, float]

items = [
    item("quarry", (5, 0, 0), "Increases rock production by 50%", (r"%rock", 0.5)),
    item("forest", (0, 5, 0), "Increases paper production by 50%", (r"%paper", 0.5)),
    item("sharp blades", (0, 0, 5), "Increases scissors production by 50%", (r"%scissors", 0.5)),
    item("catapult", (10, 10, 10), "Increases all production by 10%", (r"%scissors", 0.1)),
    item("Autoclicker", (30, 30, 30), "Doubles offline production", (r"%CUSTOM", 0)),
    item("Always on", (60, 60, 60), "Doubles offline production again", (r"%CUSTOM", 0)),
    item("End Screen", (1000, 1000, 1000), "Gives you an end screen", (r"%CUSTOM", 0))
]

@dataclass
class Pos:
    y: int
    x: int

@dataclass
class Button:
    text: str
    pos: Pos
    action: int | rps

def game_logic(uinput):
        match uinput:
            case(rps.paper, rps.rock) |\
                (rps.scissors, rps.paper) |\
                (rps.rock, rps.scissors):
                return status.win
            case(rps.rock, rps.paper) |\
                (rps.paper, rps.scissors) |\
                (rps.scissors, rps.rock):
                return status.lose
            case(rps.rock, rps.rock) |\
                (rps.paper, rps.paper) |\
                (rps.scissors, rps.scissors):
                return status.tie
            case(-1, -1):
                return status.invalid
            case _:
                raise Exception(f"unexpected game_logic value: {uinput}")