"""Player classes for Liar's Dice game."""

from abc import ABC, abstractmethod
from typing import Optional, Tuple
import random

from .dice import Bid, DiceSet

class Player(ABC):
    """Abstract base class for all players."""

    def __init__(self, player_id: int, name: str):
        """Initialize a player with ID and name."""
        self.player_id = player_id
        self.name = name
        self.dice = DiceSet(5)

    @abstractmethod
    def make_move(self, current_bid: Optional[Bid], total_dice: int, wild_ones: bool) -> Tuple[str, Optional[Bid]]:
        """
        Make a move in the game.

        Args:
            current_bid: The current bid to respond to, or None if first bid
            total_dice: Total number of dice in play
            wild_ones: Whether ones are wild

        Returns:
            Tuple of (move_type, new_bid), where move_type is either 'bid' or 'challenge'
            and new_bid is the new bid if move_type is 'bid', None otherwise
        """
        pass

    def remove_die(self) -> bool:
        """Remove one die from the player's set."""
        return self.dice.remove_die()

    def roll_dice(self) -> None:
        """Roll all dice."""
        self.dice.roll()

    def is_active(self) -> bool:
        """Check if player is still in the game."""
        return len(self.dice) > 0

class HumanPlayer(Player):
    """Human player implementation."""

    def make_move(self, current_bid: Optional[Bid], total_dice: int, wild_ones: bool) -> Tuple[str, Optional[Bid]]:
        """Get move from human input."""
        print(f"\nYour dice: {self.dice.values}")
        
        if current_bid:
            print(f"Current bid: {current_bid.quantity} {current_bid.value}'s")
            while True:
                choice = input("Enter 'b' to bid or 'c' to challenge: ").lower()
                if choice == 'c':
                    return 'challenge', None
                elif choice == 'b':
                    break
                print("Invalid choice. Please try again.")

        while True:
            try:
                quantity = int(input("Enter quantity: "))
                value = int(input("Enter face value (1-6): "))
                
                if quantity < 1 or value < 1 or value > 6:
                    print("Invalid input. Quantity must be positive, value between 1-6.")
                    continue
                    
                new_bid = Bid(quantity, value, self.player_id)
                if not current_bid or new_bid.is_valid_raise(current_bid):
                    return 'bid', new_bid
                print("Invalid bid. Must raise quantity or value.")
            except ValueError:
                print("Invalid input. Please enter numbers.")

class AIPlayer(Player):
    """AI player implementation with basic strategy."""

    def make_move(self, current_bid: Optional[Bid], total_dice: int, wild_ones: bool) -> Tuple[str, Optional[Bid]]:
        """Make AI move based on probability and current game state."""
        if not current_bid:
            # Initial bid: bid based on own dice
            my_highest = max(self.dice.values)
            my_count = self.dice.count_value(my_highest, wild_ones)
            return 'bid', Bid(my_count, my_highest, self.player_id)

        # Calculate probability of current bid being true
        target_count = current_bid.quantity
        own_count = self.dice.count_value(current_bid.value, wild_ones)
        remaining_dice = total_dice - len(self.dice)
        
        # Estimate probability of bid being valid
        prob_per_die = 1/6 if not wild_ones else 2/6
        expected_others = remaining_dice * prob_per_die
        expected_total = own_count + expected_others
        
        if expected_total < target_count * 0.7:  # Challenge if probability seems low
            return 'challenge', None
            
        # Otherwise raise the bid
        if random.random() < 0.7:  # 70% chance to raise quantity
            return 'bid', Bid(current_bid.quantity + 1, current_bid.value, self.player_id)
        else:  # 30% chance to raise value
            return 'bid', Bid(max(1, current_bid.quantity - 1), 
                            min(6, current_bid.value + 1), 
                            self.player_id)
