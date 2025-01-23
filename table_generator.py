from typing import List
from die import Die

class TableGenerator:
    @staticmethod
    def generate_table(dice: List[Die]) -> None:
        print("\nProbability Table:")
        print("\t" + "\t".join([f"Die {i}" for i in range(len(dice))]))
        for i, die1 in enumerate(dice):
            row = [f"Die {i}"]
            for j, die2 in enumerate(dice):
                row.append(TableGenerator._calculate_probability(die1, die2))
            print("\t".join(row))

    @staticmethod
    def _calculate_probability(die1: Die, die2: Die) -> str:
        wins = 0
        total = len(die1) * len(die2)

        for x in die1:
            for y in die2:
                if x > y:
                    wins += 1

        return f"{(wins / total):.2f}"