"""Main entry point for Liar's Dice game."""

import argparse
import logging
from game.game import LiarsDice

def main():
    """Run the Liar's Dice game."""
    parser = argparse.ArgumentParser(description="Liar's Dice Game")
    parser.add_argument('--ai-players', type=int, default=1,
                      help='Number of AI opponents (default: 1)')
    parser.add_argument('--wild-ones', action='store_true',
                      help='Enable wild ones mode where 1s count as any value')
    parser.add_argument('--debug', action='store_true',
                      help='Enable debug logging')

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    print("\nWelcome to Liar's Dice!")
    print("======================")
    
    if args.wild_ones:
        print("\nPlaying with wild ones mode enabled!")
    
    print(f"\nStarting game with {args.ai_players} AI opponent(s)...")
    
    game = LiarsDice(num_ai_players=args.ai_players, wild_ones=args.wild_ones)
    game.play_game()

if __name__ == "__main__":
    main()
