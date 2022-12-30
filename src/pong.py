# pong.py
# date: 28-dec-2022
# author: jelmore

import os
import sys
import random
import time
import pygame
from pygame.locals import *

# Place window in center of user's screen
os.environ['SDL_VIDEO_CENTERED'] = '1'


class Ball:
    def __init__(self):
        self.ball = None
        self._ball_left_pixel, self._ball_top, self._ball_width, self._ball_height = 0, 0, 0, 0
        self._screen_width, self._screen_height = 0, 0
        self.speed = []

    def init_ball(self, left: int, top: int, width: int, height: int,
                  screen_width: int, screen_height: int) -> (Rect, list):
        self._ball_left_pixel, self._ball_top, self._ball_width, self._ball_height = left, top, width, height
        self._screen_width, self._screen_height = screen_width, screen_height
        self.ball = pygame.Rect(self._ball_left_pixel,
                                self._ball_top,
                                self._ball_width,
                                self._ball_height)
        self.speed = [random.choice([-(int(0.0085 * self._screen_width)),
                                     -(int(0.0075 * self._screen_width)),
                                     int(0.0085 * self._screen_width),
                                     int(0.0075 * self._screen_width)]),
                      random.choice([-(int(0.0075 * self._screen_height)),
                                     -(int(0.005 * self._screen_height)),
                                     0,
                                     int(0.005 * self._screen_height),
                                     int(0.0075 * self._screen_height)])]
        print(f"self.ball: {self.ball}")
        # print(f"type(self.ball): {type(self.ball)}")
        print(f"self.speed: {self.speed}")
        return self.ball, self.speed


class Player:
    def __init__(self):
        self.score = 0
        self.paddle = (None, None)
        self._left, self._top, self._width, self._height = 0, 0, 0, 0

    def get_player_score(self) -> int:
        return self.score

    def add_score(self) -> int:
        self.score += 1
        return self.score

    def init_paddle(self, left: int, top: int, width: int, height: int) -> tuple:
        self._left, self._top, self._width, self._height = left, top, width, height
        self.paddle = (self._left, self._top, self._width, self._height)
        return self.paddle

    def get_paddle_loc(self) -> tuple:
        return self.paddle

    def update_paddle_loc(self, top: int) -> tuple:
        self._top = top  # Update top location
        # print(f'self._top: {self._top}')
        self.paddle = (self._left, self._top, self._width, self._height)
        return self.paddle


class Pong:
    def __init__(self):
        self._running = True
        self._screen = None
        self._yellow, self._white, self._p1_color, self._p2_color, self._ball_color = (), (), (), (), ()
        self._left_top_bar_pixel, self._right_top_bar_pixel, self._top_bar_top_pixel, \
            self._top_bar_height, self._top_bar = 0, 0, 0, 0, 0
        self._bottom_bar, self._bottom_bar_top = 0, 0
        self._center_left_pixel, self._center_line_top, self._center_line_width, self._center_line_height, \
            self._center_line = 0, 0, 0, 0, 0
        # self.size = self.width, self.height = 858, 525  # Original Atari screen resolution
        self.size = self.width, self.height = 1920, 1080
        self._main_clock = pygame.time.Clock()  # Set clock
        self._font = None
        self.player1, self.player2 = None, None
        self._last_hit = None
        self._font_size = 0
        self._p1_score_loc, self._p2_score_loc = 0, 0
        self._p1_paddle_loc, self._p2_paddle_loc = (None, None), (None, None)
        self._y_bounds = []
        self.p1_paddle, self.p2_paddle = (), ()
        self._paddle_move_incr = 0
        self._paddle_width, self._paddle_height = 0, 0
        self.ball = None
        self.speed = []
        self._ball_left_pixel, self._ball_top, self._ball_width, self._ball_height = 0, 0, 0, 0
        self._paddle_bounce_s, self._wall_bounce_s, self._out_of_bounds_s = None, None, None

    def on_init(self):
        # Setup pygame mixer
        pygame.mixer.pre_init(44100, -16, 2, 512)

        # Init pygame
        pygame.init()
        self._screen = pygame.display.set_mode(self.size, pygame.SHOWN | pygame.DOUBLEBUF)
        self._running = True

        # SETUP SCREEN
        # Colors
        self._yellow = (235, 229, 52)
        self._white = (245, 245, 245)
        self._p1_color = (222, 117, 31)
        self._p2_color = (83, 214, 56)
        self._ball_color = (60, 68, 214)

        # Top bar setup
        self._left_top_bar_pixel = int(self.width * 0.035)
        self._right_top_bar_pixel = self.width - int(2 * self._left_top_bar_pixel)
        self._top_bar_top_pixel = int(self.height * 0.171)
        self._top_bar_height = int(self._left_top_bar_pixel / 3)
        self._top_bar = pygame.Rect(self._left_top_bar_pixel,
                                    self._top_bar_top_pixel,
                                    self._right_top_bar_pixel,
                                    self._top_bar_height)

        # Bottom bar setup
        self._bottom_bar_top = int(self.height * 0.9)
        self._bottom_bar = pygame.Rect(self._left_top_bar_pixel,
                                       self._bottom_bar_top,
                                       self._right_top_bar_pixel,
                                       self.height * 0.1)

        # Center line setup
        self._center_left_pixel = int(self.width / 2)  # - int(self.width * 0.015)
        self._center_line_top = int(self._top_bar_top_pixel + 2 * self._top_bar_height)
        self._center_line_width = self._top_bar_height
        self._center_line_height = int(self._bottom_bar_top * 0.075)
        # print(f"self._center_line_height = {self._center_line_height}")
        self._center_line = pygame.Rect(self._center_left_pixel,
                                        self._center_line_top,
                                        self._center_line_width,
                                        self._center_line_height)

        pygame.display.set_caption("Pong-23")  # Set window title

        # Setup font
        self._font_size = int(self.width * 0.075)
        self._font = pygame.font.Font("data/fonts/EightBit-Atari-Block.ttf", self._font_size)

        # Setup score location
        self._p1_score_loc = (int(self.width / 5), int(self.height * 0.001))
        self._p2_score_loc = (3.5 * int(self.width / 5), int(self.height * 0.001))

        # Initialize players
        self.player1, self.player2 = Player(), Player()

        # Paddle setup
        # self._paddle_move_incr = int(self.height * 0.0075)
        self._paddle_move_incr = int(self.height * 0.01)
        # p1
        p1_x = self._left_top_bar_pixel
        y = int(self.height / 2)
        self._paddle_width = int(1.1 * self._top_bar_height)
        self._paddle_height = int(self._center_line_height * 1.1)
        self.player1.init_paddle(p1_x,
                                 y,
                                 self._paddle_width,
                                 self._paddle_height)

        # p2
        p2_x = self._right_top_bar_pixel + 1.8 * self._paddle_width
        self.player2.init_paddle(p2_x,
                                 y,
                                 self._paddle_width,
                                 self._paddle_height)

        # Y-boundary setup (top pixel bound, bottom pixel bound)
        # print(f" self._top_bar_top_pixel :: self._top_bar_height: {self._top_bar_top_pixel} : {self._top_bar_height}")
        self._y_bounds = [self._top_bar_top_pixel + self._top_bar_height, self._bottom_bar_top - self._paddle_height]

        # Initialize and setup ball
        self._ball_left_pixel = self._center_left_pixel
        self._ball_top = int((((self._bottom_bar_top - (self._top_bar_top_pixel + self._top_bar_height)) / 2) +
                              self._top_bar_top_pixel) * 1.025)
        self._ball_width = self._ball_height = self._center_line_width
        self.ball, self.speed = Ball().init_ball(self._ball_left_pixel,
                                                 self._ball_top,
                                                 self._ball_width,
                                                 self._ball_height,
                                                 self.width,
                                                 self.height)

        # Setup key repeat frequency (delay, interval)
        pygame.key.set_repeat(50, 10)

        # Setup sounds
        pygame.mixer.set_num_channels(32)
        self._paddle_bounce_s = pygame.mixer.Sound('data/sfx/4365__noisecollector__pongblipa5.wav')
        self._wall_bounce_s = pygame.mixer.Sound('data/sfx/4371__noisecollector__pongblipc4.wav')
        self._out_of_bounds_s = pygame.mixer.Sound('data/sfx/475347__fupicat__videogame-death-sound.wav')
        self._paddle_bounce_s.set_volume(0.6)
        self._wall_bounce_s.set_volume(0.8)
        self._out_of_bounds_s.set_volume(1.0)


    def on_event(self, event):
        if event.type == pygame.QUIT or \
           (event.type == KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)):  # Quit if we press
            self._running = False

        keys = pygame.key.get_pressed()
        # if event.type == KEYDOWN and event.key == pygame.K_w:  # Player 1 keys: w, s (up, down)
        if keys[pygame.K_w]:  # Player 1 keys: w, s (up, down)
            # print(f"self.player1.get_paddle_loc[1]: {self.player1.get_paddle_loc()[1]}")
            # print(f"self._y_bounds: {self._y_bounds}")
            if self.player1.get_paddle_loc()[1] <= (self._y_bounds[0] + self._paddle_move_incr):
                # If we exceed top bar coords, block the paddle from moving any further
                self.player1.update_paddle_loc(self._y_bounds[0])
            elif self.player1.get_paddle_loc()[1] > self._y_bounds[0]:
                self.player1.update_paddle_loc(self.player1.get_paddle_loc()[1] - self._paddle_move_incr)
        if keys[pygame.K_s]:
            # print(f"self.player1.get_paddle_loc[1]: {self.player1.get_paddle_loc()[1]}")
            # print(f"self._y_bounds: {self._y_bounds}")
            if self.player1.get_paddle_loc()[1] >= (self._y_bounds[1] - self._paddle_move_incr):
                # If we exceed top bar coords, block the paddle from moving any further
                self.player1.update_paddle_loc(self._y_bounds[1])
            elif self.player1.get_paddle_loc()[1] < self._y_bounds[1]:
                self.player1.update_paddle_loc(self.player1.get_paddle_loc()[1] + self._paddle_move_incr)
        if keys[pygame.K_UP]:  # Player 2 keys: up, down (up, down)
            # print(f"self.player2.get_paddle_loc[1]: {self.player2.get_paddle_loc()[1]}")
            # print(f"self._y_bounds: {self._y_bounds}")
            if self.player2.get_paddle_loc()[1] <= (self._y_bounds[0] + self._paddle_move_incr):
                # If we exceed top bar coords, block the paddle from moving any further
                self.player2.update_paddle_loc(self._y_bounds[0])
            elif self.player2.get_paddle_loc()[1] > self._y_bounds[0]:
                self.player2.update_paddle_loc(self.player2.get_paddle_loc()[1] - self._paddle_move_incr)
        if keys[pygame.K_DOWN]:
            # print(f"self.player2.get_paddle_loc[1]: {self.player2.get_paddle_loc()[1]}")
            # print(f"self._y_bounds: {self._y_bounds}")
            if self.player2.get_paddle_loc()[1] >= (self._y_bounds[1] - self._paddle_move_incr):
                # If we exceed top bar coords, block the paddle from moving any further
                self.player2.update_paddle_loc(self._y_bounds[1])
            elif self.player2.get_paddle_loc()[1] < self._y_bounds[1]:
                self.player2.update_paddle_loc(self.player2.get_paddle_loc()[1] + self._paddle_move_incr)

    def on_loop(self):
        # Move ball
        self.ball = self.ball.move(self.speed)
        # print(f"Game loop: self.ball: {self.ball}")

        # Test if the ball has collided w/ either paddle or the top/bottom walls
        p1_paddle = pygame.Rect(self.player1.get_paddle_loc())
        p2_paddle = pygame.Rect(self.player2.get_paddle_loc())
        if p1_paddle.collidepoint(self.ball.x - int(self.ball.width / 2), self.ball.y):
            print(f"\nBall collided w/ player 1 at ball coords: {self.ball.x, self.ball.y}")
            print(f"Player 1 paddle collided w/ ball at paddle coords: {p1_paddle.x, p1_paddle.y}")
        if p2_paddle.collidepoint(self.ball.x + self.ball.width, self.ball.y):
            print(f"\nBall collided w/ player 2 at coords: {self.ball.x, self.ball.y}")
            print(f"Player 2 paddle collided w/ ball at paddle coords: {p2_paddle.x, p2_paddle.y}")
        if self.ball.left < 0 or self.ball.right > self.width:
            self._out_of_bounds_s.play()  # Sound effect
            # Increment score
            if self._last_hit is None:
                pass
            elif self._last_hit == "p1":
                self.player1.add_score()
            elif self._last_hit == "p2":
                self.player2.add_score()

            if self.player1.get_player_score() == 11:
                print(f"PLAYER 1 WINS!")
                self.game_over("p1")
            elif self.player2.get_player_score() == 11:
                print(f"PLAYER 2 WINS!")
                self.game_over("p2")
            time.sleep(2.5)
            # If we've gone past the left/right screen boundaries, re-init the ball
            self.ball, self.speed = Ball().init_ball(self._ball_left_pixel,
                                                     self._ball_top,
                                                     self._ball_width,
                                                     self._ball_height,
                                                     self.width,
                                                     self.height)
            # Re-init _last_hit so we don't inadvertently give a point to a player who hasn't hit the ball
            self._last_hit = None
            # self.speed[0] = -self.speed[0]
        # if self.ball.top < 0 or self.ball.bottom > self.height:

        # Wall bounce
        # This seems to work better than pygame.Rect.colliderrect()
        if self.ball.top <= (self._y_bounds[0]) or self.ball.bottom > (self._y_bounds[1] + self._paddle_height):
            self._wall_bounce_s.play()  # Sound effect
            self.speed[1] = -self.speed[1]
        elif p1_paddle.collidepoint(self.ball.x - int(self.ball.width / 2), self.ball.y):
            self._paddle_bounce_s.play()  # Sound effect
            self._last_hit = "p1"
            print(f'(p1_paddle.x - self.ball.x) / self.height = {(p1_paddle.x - self.ball.x) / self.height}')
            print(f'abs(self.speed[1] / self.height) = {abs(self.speed[1] / self.height)}')
            if abs(self.speed[1] / self.height) > 0.0138:
                self.speed[1] /= 2
            elif int(self.speed[1]) == 0:
                self.speed[1] = random.choice([-(int(0.0075 * self.height)),
                                               -(int(0.005 * self.height)),
                                               0,
                                               int(0.005 * self.height),
                                               int(0.0075 * self.height)])
            elif abs((p1_paddle.x - self.ball.x) / self.height) >= 0.015:
                self.speed[1] *= 1.1
            elif abs((p1_paddle.x - self.ball.x) / self.height) < 0.015:
                self.speed[1] *= 0.95
            self.speed[0] = -self.speed[0]
            print(f'Update: self.speed = {self.speed}')
        elif p2_paddle.collidepoint(self.ball.x + self.ball.width, self.ball.y):
            self._paddle_bounce_s.play()  # Sound effect
            self._last_hit = "p2"
            print(f'(p2_paddle.x - self.ball.x) / self.height = {(p2_paddle.x - self.ball.x) / self.height}')
            print(f'abs(self.speed[1] / self.height) = {abs(self.speed[1] / self.height)}')
            if abs(self.speed[1] / self.height) > 0.0138:
                self.speed[1] /= 2
            elif int(self.speed[1]) == 0:
                self.speed[1] = random.choice([-(int(0.0075 * self.height)),
                                               -(int(0.005 * self.height)),
                                               0,
                                               int(0.005 * self.height),
                                               int(0.0075 * self.height)])
            elif abs((p2_paddle.x - self.ball.x) / self.height) >= 0.015:
                self.speed[1] *= 1.1
            elif abs((p2_paddle.x - self.ball.x) / self.height) < 0.015:
                self.speed[1] *= 0.95
            self.speed[0] = -self.speed[0]
            print(f'Update: self.speed = {self.speed}')

    def on_render(self):
        # Erase previous screen
        self._screen.fill((0, 0, 0))

        # Draw top bar
        pygame.draw.rect(self._screen, self._yellow, self._top_bar)

        # Draw center line
        new_center_line_top = self._center_line_top  # initialize at existing y value
        for _ in range(0, 8):
            self._center_line.y = new_center_line_top
            pygame.draw.rect(self._screen, self._yellow, self._center_line)  # Draw next center line
            # print(f"new_center_line_top: {new_center_line_top}")
            # print(f"self._center_line: {self._center_line}")
            # print(f"self._center_line_top: {self._center_line_top}\n")
            new_center_line_top += self._center_line_height + self._top_bar_height  # Increment y value

        # Draw bottom bar
        pygame.draw.rect(self._screen, self._white, self._bottom_bar)

        # (Re)draw paddle location as needed
        pygame.draw.rect(self._screen, self._p1_color, pygame.Rect(self.player1.get_paddle_loc()))
        pygame.draw.rect(self._screen, self._p2_color, pygame.Rect(self.player2.get_paddle_loc()))

        # Show player scores
        player1_score = self._font.render(str(self.player1.get_player_score()), True, self._p1_color)
        player2_score = self._font.render(str(self.player2.get_player_score()), True, self._p2_color)
        self._screen.blit(player1_score, self._p1_score_loc)
        self._screen.blit(player2_score, self._p2_score_loc)

        # Draw ball
        pygame.draw.rect(self._screen, self._ball_color, self.ball)

        # Refresh display w/ updated info
        # pygame.display.flip()
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def game_over(self, winner: str):
        # TODO: Add game over text and winner announcement
        pass

    def on_execute(self):
        if self.on_init() is False:
            self._running = False

        while self._running:
            # Set framerate to 30 fps
            self._main_clock.tick(30)

            # Check for events
            for event in pygame.event.get():
                self.on_event(event)

            # Do loop stuff
            self.on_loop()

            # Render new screen
            self.on_render()
        self.on_cleanup()  # Only perform cleanup if we want/need to exit
        # sys.exit()


if __name__ == "__main__":
    pong = Pong()
    pong.on_execute()
