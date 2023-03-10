Name: pong.py

Description: My simple implementation of classic Pong.

Author: 
  - Code: jelmore
  - Fonts: https://github.com/TheRobotFactory/EightBit-Atari-Fonts
  - WAVs: 
    - wall/paddle collision: https://freesound.org/people/NoiseCollector/
    - score/out-of-bounds: https://freesound.org/people/Fupicat/
    - start game: https://freesound.org/people/iut_Paris8/

Usage:
  1. Clone repository: `git clone https://github.com/jerryrelmore/1-pong-23.git`
  2. `cd 1-pong-23/src`
  3. Either setup a virtual env or install requirements as a system package, e.g.: `pip3 install -r ../requirements.txt`
  4. Execute: `python3 pong.py`
  5. Player 1 uses `w` and `s` to move up or down, respectively.
  6. Player 2 uses `UP` and `DOWN` arrows for the same.
  7. Press `r` to restart the game at any time.
  8. Press `q` or `ESC` to quit.
  9. First player to 11 points wins.
Enjoy!

#TODO:
  1. ~~Implement Game Over screen.~~
  2. ~~Implement ability to restart during the game.~~
  3. ~~End game when first player scores 11 points.~~
  4. Add jingle for winner.
  5. Add slight pause before ball moves after restart (maybe leverage self._first_run bool?).
  6. Add ability to pass in preferred screen size as CLI arg.
  7. ???
  8. Code clean-up

#BUGFIX:
  1. If upper-left pixel of ball has a lower value than upper left pixel of the paddle, a collision isn't detected.
  2. Ball can get "stuck" on paddle and bounce quickly back and forth then end up going behind the capturing paddle. NOTE:
     May actually consider this a feature, not a bug.

Gameplay screenshot:
![Gameplay Screenshot](/src/data/images/gameplay_screen.png?raw=true "Gamplay")
