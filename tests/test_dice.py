"""Tests for dice-related functionality."""

import pytest
from src.game.dice import Bid, DiceSet

def test_bid_validation():
    """Test bid validation logic."""
    bid1 = Bid(2, 3, 1)  # 2 threes
    bid2 = Bid(3, 3, 2)  # 3 threes
    bid3 = Bid(2, 4, 3)  # 2 fours
    
    assert bid2.is_valid_raise(bid1)  # Higher quantity, same face
    assert bid3.is_valid_raise(bid1)  # Higher face
    assert not bid1.is_valid_raise(bid2)  # Lower quantity

def test_dice_set():
    """Test DiceSet functionality."""
    dice = DiceSet(5)
    
    # Test initial state
    assert len(dice) == 5
    assert len(dice.values) == 5
    assert all(1 <= v <= 6 for v in dice.values)
    
    # Test rolling
    old_values = dice.values.copy()
    dice.roll()
    assert len(dice.values) == 5
    assert all(1 <= v <= 6 for v in dice.values)
    
    # Test removing dice
    assert dice.remove_die()
    assert len(dice) == 4
    
    # Test counting values
    test_dice = DiceSet(3)
    test_dice.values = [1, 2, 2]  # Force specific values
    assert test_dice.count_value(2) == 2
    assert test_dice.count_value(1) == 1
    assert test_dice.count_value(3) == 0
    
    # Test wild ones
    assert test_dice.count_value(2, wild_ones=True) == 3  # 2 twos + 1 wild one
