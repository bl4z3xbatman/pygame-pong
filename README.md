# Pygame Pong

A simple 2D Pong game built with Python and Pygame Community Edition.

Features:
- Single-player mode against a CPU opponent
- Local two-player mode using one keyboard
- Main menu to pick game mode
- High-score tracking for single-player survival time
- Unlockable paddle colors with a color selection screen
- Clean Model-View-Controller (MVC) structure

## Setup

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Controls

Single-player:
- Left paddle: W / S
- Right paddle: CPU controlled
- Press C in the menu to choose a paddle color

Two-player:
- Left paddle: W / S
- Right paddle: Up / Down

Menu:
- Press 1 for one player
- Press 2 for two players
- Press C to adjust your paddle color
- Press Esc to return to the menu during play

## Paddle Colors

Your paddle color unlocks based on how long you survive in single-player mode without conceding a point.

- Classic White: unlocked by default
- Blue: 10 seconds survival
- Red: 25 seconds survival
- Green: 45 seconds survival
- Gold: 60 seconds survival
