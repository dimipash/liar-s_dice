"""Dice related functionality for the Liar's Dice game."""

import random
from dataclasses import dataclass
from typing import List

@dataclass
class Bid:
    """Represents a bid in the game."""
    quantity: int
    value: int
    player_id: int

    def is_valid_raise(self, other: 'Bid') -> bool:
        """Check if this bid is a valid raise over another bid."""
        if self.value == other.value:
            return self.quantity > other.quantity
        elif self.value > other.value:
            return True
        return False

class DiceSet:
    """Represents a set of dice for a player."""
    
    def __init__(self, num_dice: int = 5):
        """Initialize dice set with given number of dice."""
        self.num_dice = num_dice
        self.values: List[int] = []
        self.roll()

    def roll(self) -> None:
        """Roll all dice in the set."""
        self.values = [random.randint(1, 6) for _ in range(self.num_dice)]

    def count_value(self, value: int, wild_ones: bool = False) -> int:
        """
        Count occurrences of a value in the dice set.
        
        Args:
            value: The face value to count
            wild_ones: If True, count 1s as matching any value
        """
        count = self.values.count(value)
        if wild_ones and value != 1:
            count += self.values.count(1)
        return count

    def remove_die(self) -> bool:
        """
        Remove one die from the set.
        
        Returns:
            bool: True if die was removed, False if no dice remain
        """
        if self.num_dice > 0:
            self.num_dice -= 1
            self.roll()
            return True
        return False

    def __len__(self) -> int:
        """Return the number of dice in the set."""
        return self.num_dice
