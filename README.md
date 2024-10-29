# Liar's Dice Game

A Python implementation of the classic Liar's Dice game featuring AI opponents.

## Features

- Support for 2+ players (human vs AI bots)
- Each player starts with 5 dice
- Turn-based bidding system
- Choice to raise bid or challenge previous bid
- Automatic dice reduction for round losers
- Game continues until one player remains
- Optional "wild ones" mode where 1's count as current bid value

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the game:
```bash
python src/main.py
```

## Game Rules

1. Players roll concealed dice each round
2. First player bids (quantity + face value)
3. Next player must either:
   - Raise bid (higher quantity of same face or any quantity of higher face)
   - Challenge previous bid as "liar"
4. On challenge:
   - If bid valid: challenger loses die
   - If bid invalid: bidder loses die
5. Loser starts next round
6. Last player with dice wins
