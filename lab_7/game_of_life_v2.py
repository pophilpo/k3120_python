import pygame
from pygame.locals import *
from pprint import pprint as pp
import random
import sys
import copy


class GameOfLife:

    def __init__(self, size, randomize: bool=True, max_generations=None) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_grid = self.create_grid()
        # Текущее поколение клеток
        self.curr_grid = self.create_grid(randomize)
        # Максимальное число поколений
        self.max_generations = max_generations


        # Текущее число поколений
        self.generations = 1

        self.clock = pygame.time.Clock()

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
        pass

    def save(self, filename):
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        pass
    


def main():

    life = GameOfLife((5, 10), max_generations=50)

    while life.is_changing and not life.is_max_generations_exceeded:
        life.step()
    print(life.generations)

if __name__ == "__main__":
    main()