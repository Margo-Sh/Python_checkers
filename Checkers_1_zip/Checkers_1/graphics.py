import pygame
import sys
import time
import game_logic

# DISPLAY
pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# initializing the pygame window
pg.init()

# setting fps manually
fps = 10

# this is used to track time
CLOCK = pg.time.Clock()

# this method is used to build the
# infrastructure of the display
screen = pg.display.set_mode((width, height + 100), 0, 32)

# setting up a nametag for the
# game window
pg.display.set_caption("Check out our Checkers")

# loading the images as python object
initiating_window = pg.image.load("board.png")
x_img = pg.image.load("white_checker.png")
y_img = pg.image.load("black_checker.png")

# resizing images
initiating_window = pg.transform.scale(initiating_window, (width, height + 100))
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(y_img, (80, 80))

# resizing images
initiating_window = pg.transform.scale(initiating_window, (width, height + 100))
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(y_img, (80, 80))


def game_initiating_window():
    # displaying over the screen
    screen.blit(initiating_window, (0, 0))

    # updating the display
    pg.display.update()
    time.sleep(3)
    screen.fill(white)

# def draw_status():