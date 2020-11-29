import curses
import abc
import pygame
from pygame.locals import *
from pprint import pprint as pp
import random
import sys
import copy

import time


class GameOfLife:

    def __init__(self, size, randomize: bool=True, max_generations=None, speed=100, cell_size=2) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        self.cell_size = cell_size
        # Предыдущее поколение клеток
        self.prev_grid = self.create_grid()
        # Текущее поколение клеток
        self.curr_grid = self.create_grid(randomize)
        # Максимальное число поколений
        self.max_generations = max_generations

        self.screen_size = (self.rows*cell_size, self.cols*cell_size)


        # Текущее число поколений
        self.generations = 1

        self.clock = pygame.time.Clock()

        self.speed = speed

    def create_grid(self, randomize: bool=False):
        grid = list()

        for _ in range(self.rows):
            new_row = [
                random.randint(0, 1) if randomize else 0
                for _ in range(self.cols)
            ]
            grid.append(new_row)
        
        
        return grid


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
            if (cell[0] >= 0 and cell[1] >= 0 and cell[0] != self.rows and cell[1] != self.cols)
        ]

        return result



    def get_next_generation(self):

        self.prev_grid = copy.deepcopy(self.curr_grid)

        for row_number, row in enumerate(self.curr_grid):

            for column_number, value in enumerate(row):

                cell = (row_number, column_number)

                neighbours = self.get_neighbours(cell)

                alive_counter = len(
                    [
                        self.curr_grid[n_cell[0]][n_cell[1]]
                        for n_cell in neighbours
                        if self.curr_grid[n_cell[0]][n_cell[1]] == 1
                    ]
                )
                if value == 1:
                    if alive_counter == 2 or alive_counter == 3:
                        continue
                    else:
                        self.curr_grid[row_number][column_number] = 0
                else:
                    if alive_counter == 3:
                        self.curr_grid[row_number][column_number] = 1
                    else:
                        continue




    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """

        self.clock.tick()
        self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """

        return self.max_generations < self.generations



    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_grid != self.curr_grid

    @staticmethod
    def from_file(filename): 
        """
        Прочитать состояние клеток из указанного файла.
        """

        with open(filename, "r") as file:
            data = file.read()
        

        rows = data.split("\n")

        grid = list()
        for row in rows:
            new_row = list()
            for char in row:
                new_row.append(int(char))
            grid.append(new_row)


        size = (len(rows), len(rows[0]))
        life = GameOfLife(size, False)
        life.curr_grid = grid

        return life



    def save(self, filename):
        """
        Сохранить текущее состояние клеток в указанный файл.
        """

        with open(filename, "w") as file:



            for row in self.curr_grid:
                row = map(str, row)
                string_row = "".join(row)
                file.write(string_row+"\n")

        print("Successfully exported current grid state.")


class UI(abc.ABC):

    def __init__(self, life):
        self.life = life

    @abc.abstractmethod
    def run(self):
        pass


class Console(UI):
    def __init__(self, life):
        super().__init__(life)


    def draw_borders(self, screen):

        begin_x = 0
        begin_y = 0

        # Adding plus 3 so that points don't cross borders
        height = self.life.rows + 3
        width = self.life.cols + 3

        grid = screen.subwin(height,width, begin_x, begin_y)
        grid.box()
        screen.getch()
    

    def draw_grid(self, screen):

        for x, row in enumerate(self.life.curr_grid):

            for y, value in enumerate(row):

                pos_x = x + 1
                pos_y = y + 1


                if value == 1:
                    screen.addch(pos_y, pos_x, "O")
                else:
                    screen.addch(pos_y, pos_x, ".")

        screen.refresh()






    def run(self):

        screen = curses.initscr()
        self.draw_borders(screen)

        self.draw_grid(screen)
        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            self.life.step()
            self.draw_grid(screen)
            curses.napms(self.life.speed)


        curses.endwin()


class GUI(UI):

    def __init__(self, life):
        super().__init__(life)
        self.screen = pygame.display.set_mode(self.life.screen_size)


    def draw_lines(self):

        for x in range(0, self.life.rows):
            x = x * self.life.cell_size
            pygame.draw.line(
                    self.screen, pygame.Color("black"),
                    (x, 0), 
                    (x, self.life.screen_size[1])
                    )
        for y in range(0, self.life.cols):
            y = y * self.life.cell_size
            pygame.draw.line(
                    self.screen,
                    pygame.Color("black"),
                    (0, y),
                    (self.life.screen_size[0], y)

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

                #print(f"Drawing {color} at {coord_x} - {coord_y} | Value {value}")

                pygame.draw.rect(
                        self.screen,
                        color,
                        (coord_y, coord_x, self.life.cell_size, self.life.cell_size)
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

                    value = self.life.curr_grid[y][x]
                    if value==1:
                        self.life.curr_grid[y][x] = 0
                    else:
                        self.life.curr_grid[y][x] = 1
                    self.draw_grid()
                    self.draw_lines()
                    pygame.display.flip()


    def run(self):
        print(self.life.screen_size)
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        pp(self.life.curr_grid)

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


def main():

    life = GameOfLife((10, 10), True, 100, cell_size=20)
    pp(life.curr_grid)
    ui = GUI(life)
    ui.run()

if __name__ == "__main__":
    main()
