from typing import List
from die import Die

class GameState:
    def __init__(self, dice: List[Die]):
        self.original_dice = dice
        self.available_dice = dice.copy()
        self.player_die = None
        self.computer_die = None

    def select_die(self, die: Die) -> None:
        if die in self.available_dice:
            self.available_dice.remove(die)

    def reset(self) -> None:
        self.available_dice = self.original_dice.copy()
        self.player_die = None
        self.computer_die = None