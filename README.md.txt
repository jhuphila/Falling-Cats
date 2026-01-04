# Falling Cats

A 2D arcade survival game built with Python and Pygame where players dodge falling phantoms while trying to achieve the highest score possible.

Inspired by Animal Jam's Falling Phantoms minigame.

## Gameplay

- **Objective**: Survive as long as possible while avoiding falling phantoms
- **Controls**: Use `A` and `D` keys to move left and right
- **Scoring**: Your score increases with survival time
- **Challenge**: Phantoms spawn continuously with random horizontal movement patterns

## Requirements

- Python 3.x
- Pygame

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/falling-cats.git
cd falling-cats
```

2. Install dependencies:
```bash
pip install pygame-ce
```

3. Run the game:
```bash
python main.py
```

## Project Structure

```
falling-cats/
│
├── main.py           # Main game loop and state management
├── player.py         # Player class and movement logic
├── phantom.py        # Enemy class and behavior
├── button.py         # UI button component
│
├── images/           # Game sprites and UI assets
│   ├── game-menu/    # Menu button images
│   ├── player.png
│   ├── phantom.png
│   └── bg_img.png
│
└── resources/        # Audio files and game data
    ├── game_music.mp3
    ├── phantom.mp3
    ├── death.mp3
    ├── countdown_ready.wav
    ├── countdown_go.wav
    └── high_score.txt
```

## Future Enhancements

- Power-ups and collectibles
- Multiple difficulty levels
- Additional enemy types
- Character selection
- Sound settings menu

## Credits

- Inspired by Animal Jam's Falling Phantoms minigame
- Built as a personal project to learn game development with Pygame


This project is personal learning project available to anyone