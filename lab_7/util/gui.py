import pygame
from pygame.locals import *
import sys

from util.ui import UI


class GUI(UI):
    def __init__(self, life):
        super().__init__(life)
        self.screen = pygame.display.set_mode(self.life.screen_size)

    def draw_lines(self):

        for x in range(0, self.life.rows):
            x = x * self.life.cell_size
            pygame.draw.line(
                self.screen,
                pygame.Color("black"),
                (x, 0),
                (x, self.life.screen_size[1]),
            )
        for y in range(0, self.life.cols):
            y = y * self.life.cell_size
            pygame.draw.line(
                self.screen,
                pygame.Color("black"),
                (0, y),
                (self.life.screen_size[0], y),
            )

    def draw_grid(self):

        for x, row in enumerate(self.life.curr_grid):
            for y, value in enumerate(row):

                coord_x = x * self.life.cell_size
                coord_y = y * self.life.cell_size

                if value == 1:
                    color = pygame.Color("green")
                else:
                    color = pygame.Color("white")

                # print(f"Drawing {color} at {coord_x} - {coord_y} | Value {value}")

                pygame.draw.rect(
                    self.screen,
                    color,
                    (coord_x, coord_y, self.life.cell_size, self.life.cell_size),
                )

    def pause(self):

        while True:
            for event in pygame.event.get():

                if event.type == QUIT:
                    sys.exit(1)

                if event.type == KEYDOWN:
                    return

                if event.type == MOUSEBUTTONUP:

                    x, y = pygame.mouse.get_pos()

                    x = x // self.life.cell_size
                    y = y // self.life.cell_size

                    value = self.life.curr_grid[x][y]
                    if value == 1:
                        self.life.curr_grid[x][y] = 0
                    else:
                        self.life.curr_grid[x][y] = 1
                    self.draw_grid()
                    self.draw_lines()
                    pygame.display.flip()

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        while not self.life.is_max_generations_exceeded:

            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()

            if not self.life.is_changing:
                self.pause()

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(1)

                elif event.type == KEYDOWN:
                    self.pause()

            clock.tick(5)
            self.life.step()
