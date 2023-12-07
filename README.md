[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/) [![License: CC0-1.0](https://licensebuttons.net/l/zero/1.0/80x15.png)](http://creativecommons.org/publicdomain/zero/1.0/)

> Final project for ESW class. Rythme game using Raspi4 and Adafruit LCD display console.
# Dancing Dino Game

⬇️ click the thumbnail to watch video

[![DancingDino](https://github.com/Wendy-Nam/DancingDino/blob/main/img/opening/14.png)](https://www.youtube.com/watch?v=G-tjcUxmIwA "DancingDino")

## Overview
"Dancing Dino" is a rhythm-based game where players help a young dinosaur, who dreams of becoming a great dancer, achieve its dreams. The game progresses through various stages, each with increasing difficulty and unique backgrounds, reflecting the dinosaur's journey in mastering dance.

## Classes and Their Functions
- `JoystickController`: Manages joystick inputs, display initialization, and button state updates.
- `Player`: Manages the player's sprite images, updates poses, and renders animations.
- `Arrow`: Handles the movement and rendering of arrows, including their speed and direction.
- `Stage`: Oversees the game stages, including background rendering, scoring zones, arrow generation, and stage transitions.
- `Game`: Controls the main game loop and state, including the start screen, updates, and rendering.

## Game Mechanics
- Players use the joystick to input directions corresponding to the arrows moving from the top to the bottom of the screen.
- Correctly matching the arrow direction with the joystick at the right time scores points. Incorrect matches deduct points.
- The game comprises multiple stages, each with a different background and progressively harder challenges.
- The player's score increases with successful matches and decreases with failures.
- For 'hold' arrows, hold the joystick in the indicated direction and press the 'A' button until the rectangular tail passes completely.

## Installation and Setup
- Ensure you have Python and required libraries installed.
  - setup RPi SPI Enable
    In RPi Terminal
    ```
    sudo raspi-config
    Interface .. -> SPI -> Enable
    ```
  - Requirement Library
    ```
    sudo pip3 install adafruit-circuitpython-rgb-display
    
    sudo apt-get install fonts-dejavu
    ```
    & extra you need
- Clone the repository and run the game script.

## Note

Due to a malfunction in the `Adafruit 1.3" Color TFT Bonnet`'s LCD for Raspberry Pi, i switched to using the `tk` library with VNC for GUI display. The joystick and button functionalities still utilize the Adafruit module.
