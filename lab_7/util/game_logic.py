import copy
import random
import pygame

# TODO: Fix non rect grid sizes
# TODO: Fix generation logic


class Cell:
    def __init__(self, row, column):
        self.row = row
        self.column = column


class GameOfLife:
    def __init__(
        self,
        size=(5, 5),
        randomize: bool = True,
        max_generations=None,
        speed=100,
        cell_size=50,
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        self.cell_size = cell_size
        # Предыдущее поколение клеток
        self.prev_grid = self.create_grid()
        # Текущее поколение клеток
        self.curr_grid = self.create_grid(randomize)
        # Максимальное число поколений
        self.max_generations = max_generations

        self.screen_size = (self.rows * cell_size, self.cols * cell_size)

        # Текущее число поколений
        self.generations = 1

        self.clock = pygame.time.Clock()

        self.speed = speed

    def change_state(self, cell):

        self.curr_grid[cell.row][cell.column] = (
            1 if self.curr_grid[cell.row][cell.column] == 0 else 0
        )

    def create_grid(self, randomize: bool = False):
        grid = list()

        for _ in range(self.rows):
            new_row = [
                random.randint(0, 1) if randomize else 0 for _ in range(self.cols)
            ]
            grid.append(new_row)

        return grid

    def get_neighbours(self, cell):

        result = list()

        x, y = cell.row, cell.column

        X = self.rows
        Y = self.cols

        result = [
            (x2, y2)
            for x2 in range(x - 1, x + 2)
            for y2 in range(y - 1, y + 2)
            if (
                -1 < x <= X
                and -1 < y <= Y
                and (x != x2 or y != y2)
                and (0 <= x2 < X)
                and (0 <= y2 < Y)
            )
        ]

        return result

    def get_next_generation(self):

        self.prev_grid = copy.deepcopy(self.curr_grid)

        to_change = list()

        for row_number, row in enumerate(self.curr_grid):

            for column_number, value in enumerate(row):

                cell = Cell(row_number, column_number)

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
                        to_change.append(cell)
                else:
                    if alive_counter == 3:
                        to_change.append(cell)
                    else:
                        continue
        for cell in to_change:
            self.change_state(cell)

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
    def from_file(filename, max_generations):
        """
        Прочитать состояние клеток из указанного файла.
        """

        # This is so bad. I think it's due to my IDE adding newlines.
        grid = list()
        with open(filename, "r") as file:

            for row in file.readlines():
                row = row.replace("\n", "")
                if not row.isdigit():
                    continue
                new_row = list()
                for char in row:
                    new_row.append(int(char))
                grid.append(new_row)
        print(grid)

        size = (len(grid), len(grid[0]))
        life = GameOfLife(size, False, max_generations=max_generations)
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
                file.write(string_row + "\n")

        print("Successfully exported current grid state.")
