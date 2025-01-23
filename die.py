from typing import List

class Die:
    def __init__(self, values: List[int]):
        if not values:
            raise ValueError("Die must have at least one face")
        self.values = values.copy()  # Create a copy to prevent modification

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, index: int) -> int:
        return self.values[index]

    def __repr__(self) -> str:
        return f"Die({self.values})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Die):
            return False
        return self.values == other.values