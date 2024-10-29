"""Main game logic for Liar's Dice."""

import logging
from typing import List, Optional, Tuple
from .player import Player, HumanPlayer, AIPlayer
from .dice import Bid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LiarsDice:
    """Main game class implementing Liar's Dice rules and mechanics."""

    def __init__(self, num_ai_players: int = 1, wild_ones: bool = False):
        """
        Initialize the game.

        Args:
            num_ai_players: Number of AI opponents
            wild_ones: Whether ones count as any value
        """
        self.wild_ones = wild_ones
        self.players: List[Player] = [
            HumanPlayer(0, "Human Player")
        ]
        for i in range(num_ai_players):
            self.players.append(AIPlayer(i + 1, f"AI Player {i + 1}"))
        
        self.current_player_idx = 0
        self.current_bid: Optional[Bid] = None
        self.round_number = 1

    def get_total_dice(self) -> int:
        """Get total number of dice currently in play."""
        return sum(len(player.dice) for player in self.players)

    def check_bid(self, bid: Bid) -> bool:
        """
        Check if a bid is valid against actual dice.

        Args:
            bid: The bid to check

        Returns:
            bool: True if bid is valid, False otherwise
        """
        total_count = 0
        for player in self.players:
            total_count += player.dice.count_value(bid.value, self.wild_ones)
        return total_count >= bid.quantity

    def next_player(self) -> None:
        """Advance to the next active player."""
        while True:
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
            if self.players[self.current_player_idx].is_active():
                break

    def handle_challenge(self, challenger_idx: int, bid: Bid) -> int:
        """
        Handle a challenge resolution.

        Args:
            challenger_idx: Index of challenging player
            bid: The challenged bid

        Returns:
            int: Index of the losing player
        """
        bid_valid = self.check_bid(bid)
        loser_idx = challenger_idx if bid_valid else self.current_player_idx
        self.players[loser_idx].remove_die()
        
        # Log the challenge result
        total_count = sum(player.dice.count_value(bid.value, self.wild_ones) 
                         for player in self.players)
        logger.info(f"Challenge result: {'Bid valid' if bid_valid else 'Bid invalid'}")
        logger.info(f"Actual count of {bid.value}'s: {total_count}")
        
        return loser_idx

    def play_round(self) -> Optional[Player]:
        """
        Play one round of the game.

        Returns:
            Optional[Player]: The winner if game is over, None otherwise
        """
        logger.info(f"\nRound {self.round_number}")
        
        # Roll dice for all players
        for player in self.players:
            if player.is_active():
                player.roll_dice()

        self.current_bid = None
        
        while True:
            current_player = self.players[self.current_player_idx]
            if not current_player.is_active():
                self.next_player()
                continue

            # Get player's move
            move_type, new_bid = current_player.make_move(
                self.current_bid,
                self.get_total_dice(),
                self.wild_ones
            )

            if move_type == 'challenge':
                if not self.current_bid:
                    logger.error("Cannot challenge when no bid exists")
                    continue
                    
                loser_idx = self.handle_challenge(self.current_player_idx, self.current_bid)
                self.current_player_idx = loser_idx  # Loser starts next round
                break
            else:  # move_type == 'bid'
                if new_bid:
                    self.current_bid = new_bid
                    logger.info(f"{current_player.name} bids {new_bid.quantity} {new_bid.value}'s")
                    self.next_player()

        # Check for game over
        active_players = [p for p in self.players if p.is_active()]
        if len(active_players) == 1:
            return active_players[0]

        self.round_number += 1
        return None

    def play_game(self) -> Player:
        """
        Play the full game until a winner is determined.

        Returns:
            Player: The winning player
        """
        winner = None
        while not winner:
            winner = self.play_round()
            
        logger.info(f"\nGame Over! {winner.name} wins!")
        return winner
