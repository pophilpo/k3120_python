import pygame
from pygame.locals import *
from pprint import pprint as pp
import random
import sys


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        self.grid = None

    def draw_lines(self) -> None:
        # @see: http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (x, 0), (x, self.height)
            )
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (0, y), (self.width, y)
            )

    def run(self) -> None:
        pygame.init()
        self.create_grid(True)
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)
            self.get_next_generation()
        pygame.quit()

    def create_grid(self, randomize=False):

        grid = list()

        for _ in range(self.height // self.cell_size):
            new_row = [
                random.randint(0, 1) if randomize else 0
                for _ in range(self.width // self.cell_size)
            ]
            grid.append(new_row)

        self.grid = grid

    def draw_grid(self):

        for row_index, row in enumerate(self.grid):
            for column_index, value in enumerate(row):

                x, y = row_index * self.cell_size, column_index * self.cell_size
                if value == 1:
                    color = pygame.Color("green")
                else:
                    color = pygame.Color("white")

                pygame.draw.rect(
                    self.screen, color, (x, y, self.cell_size, self.cell_size)
                )

    def get_neighbours(self, cell):

        result = list()

        x = cell[0]
        y = cell[1]

        result.append((x + 1, y))
        result.append((x + 1, y + 1))
        result.append((x, y + 1))
        result.append((x - 1, y + 1))
        result.append((x - 1, y))
        result.append((x - 1, y - 1))
        result.append((x, y - 1))

        result = [
            cell
            for cell in result
            if (cell[0] >= 0 and cell[1] >= 0 and cell[0] != 12 and cell[1] != 16)
        ]

        return result

    def get_next_generation(self):

        for row_number, row in enumerate(self.grid):

            for column_number, value in enumerate(row):

                cell = (row_number, column_number)
                print(cell)

                neighbours = self.get_neighbours(cell)

                alive_counter = len(
                    [
                        self.grid[n_cell[0]][n_cell[1]]
                        for n_cell in neighbours
                        if self.grid[n_cell[0]][n_cell[1]] == 1
                    ]
                )
                if value == 1:
                    if alive_counter == 2 or alive_counter == 3:
                        continue
                    else:
                        self.grid[row_number][column_number] = 0
                else:
                    if alive_counter == 3:
                        self.grid[row_number][column_number] = 1
                    else:
                        continue


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()