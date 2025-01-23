import sys
from typing import List
from die import Die
from game_state import GameState
from crypto_provider import CryptoProvider
from fair_number_generator import FairNumberGenerator
from table_generator import TableGenerator

class GameController:
    def __init__(self, dice_values: List[List[int]]):
        if len(dice_values) < 3:
            raise ValueError("At least three dice must be provided")
        self.crypto_provider = CryptoProvider()
        self.fair_generator = FairNumberGenerator(self.crypto_provider)
        dice = [Die(values) for values in dice_values]
        self.state = GameState(dice)

    def start_game(self) -> None:
        print("Welcome to the Dice Game!")
        TableGenerator.generate_table(self.state.original_dice)

        print("\nLet's determine who will select their die first.")
        player_first = self._determine_first_player()

        if player_first:
            print("You will select your die first.")
            self.state.player_die = self._player_select_die()
            self.state.computer_die = self._computer_select_die()
        else:
            print("Computer will select its die first.")
            self.state.computer_die = self._computer_select_die()
            self.state.player_die = self._player_select_die()

        print(f"\nYou selected: {self.state.player_die}")
        print(f"Computer selected: {self.state.computer_die}")

        print("\nTime to roll the dice!")
        player_score = self._make_throw("Your throw", self.state.player_die)
        computer_score = self._make_throw("Computer's throw", self.state.computer_die)

        print(f"\nYour score: {player_score}")
        print(f"Computer's score: {computer_score}")

        if player_score > computer_score:
            print("Congratulations, you win!")
        elif player_score < computer_score:
            print("Sorry, the computer wins.")
        else:
            print("It's a tie!")

    def _determine_first_player(self) -> bool:
        computer_num, key, hmac_value = self.fair_generator.generate_fair_number(1)
        print(f"I selected a random number (HMAC={hmac_value}).")
        print("Guess the number: 0 or 1")

        while True:
            choice = input("Your guess: ").strip()
            if choice not in ('0', '1'):
                print("Invalid choice. Please enter 0 or 1.")
                continue
            player_guess = int(choice)
            print(f"My number is {computer_num} (KEY={key.hex().upper()}).")
            return player_guess == computer_num

    def _computer_select_die(self) -> Die:
        available = self.state.available_dice
        if not available:
            raise ValueError("No dice available for selection")
        
        computer_choice = self.crypto_provider.generate_uniform_random(len(available) - 1)
        selected_die = available[computer_choice]
        self.state.select_die(selected_die)
        return selected_die

    def _player_select_die(self) -> Die:
        available = self.state.available_dice
        print("Choose your dice:")
        for i, die in enumerate(available):
            print(f"{i} - {die}")

        while True:
            choice = input("Your selection: ").strip()
            if not choice.isdigit() or int(choice) >= len(available):
                print("Invalid selection. Please try again.")
                continue
            selected_die = available[int(choice)]
            self.state.select_die(selected_die)
            return selected_die

    def _make_throw(self, context: str, die: Die) -> int:
        computer_num, key, hmac_value = self.fair_generator.generate_fair_number(len(die) - 1)
        print(f"{context}: I selected a random value in the range 0..{len(die) - 1} (HMAC={hmac_value}).")
        print("Add your number modulo the die size.")

        for i in range(len(die)):
            print(f"{i} - {die[i]}")

        while True:
            choice = input("Your selection: ").strip()
            if not choice.isdigit() or int(choice) >= len(die):
                print("Invalid selection. Please try again.")
                continue
            player_num = int(choice)
            result = (player_num + computer_num) % len(die)
            print(f"My number is {computer_num} (KEY={key.hex().upper()}).")
            print(f"The result is {player_num} + {computer_num} = {result} (mod {len(die)}).")
            return die[result]