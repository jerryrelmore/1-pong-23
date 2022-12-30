Name: pong.py

Description: My simple implementation of classic Pong.

Author: 
  - Code: jelmore
  - Fonts: https://github.com/TheRobotFactory/EightBit-Atari-Fonts
  - WAVs: 
    - wall/paddle collision: https://freesound.org/people/NoiseCollector/packs/254/
    - score/out-of-bounds: https://freesound.org/people/Fupicat/sounds/475347/

Usage:
  1. Clone repository: `git clone https://github.com/jerryrelmore/1-pong-23.git`
  2. `cd 1-pong-23/src`
  3. Either setup a virtual env or install requirements as a system package, e.g.: `pip3 install -r ../requirements.txt`
  4. Execute: `python3 pong.py`
  5. Player 1 uses `w` and `s` to move up or down, respectively.
  6. Player 2 uses `UP` and `DOWN` arrows for the same.
  7. Press `q` or `ESC` to quit.
Enjoy!

#TODO:
  1. Implement Game Over screen.
  2. Implement ability to restart during the game.
  3. End game when first player scores 11 points.
  4. ???
  5. Clean-up

#BUGFIX:
  1. If upper-left pixel of ball has a lower value than upper left pixel of the paddle, a collision isn't detected.
  2. Ball can get "stuck" on paddle and bounce quickly back and forth then end up going behind the capturing paddle. NOTE:
     May actually consider this a feature, not a bug.

Gameplay screenshot:
![Gameplay Screenshot](/src/data/images/gameplay_screen.png?raw=true "Gamplay")
