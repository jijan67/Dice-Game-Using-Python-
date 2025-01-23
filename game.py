import sys
from typing import List
from game_controller import GameController

def parse_dice_input(args: List[str]) -> List[List[int]]:
    dice_values = []
    for arg in args:
        try:
            values = [int(x) for x in arg.split(',')]
            if not values:
                raise ValueError("Empty dice values")
            dice_values.append(values)
        except ValueError as e:
            print(f"Error parsing dice values '{arg}': {e}")
            sys.exit(1)
    return dice_values

def main() -> None:
    if len(sys.argv) < 4:  # Require at least 3 dice
        print("Usage: python game.py dice1 dice2 dice3 [dice4 ...]")
        print("Example: python game.py 1,2,3,4,5,6 1,1,1,6,6,6 2,2,2,5,5,5")
        sys.exit(1)

    try:
        dice_values = parse_dice_input(sys.argv[1:])
        game = GameController(dice_values)
        game.start_game()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()