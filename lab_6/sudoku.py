import pathlib
import typing as tp
from random import shuffle
import random

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    with open(path, "r") as file:
        puzzle = file.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "")
                for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """

    result = list()
    for index in range(0, len(values), n):
        result.append(values[index : index + n])
    return result


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """

    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """

    result = list()

    for row in grid:
        result.append(row[pos[1]])

    return result


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """

    x_start = (pos[0] // 3) * 3
    y_start = (pos[1] // 3) * 3

    result = list()

    for row_index in range(x_start, x_start + 3):

        row = grid[row_index][y_start : y_start + 3]
        result = result + row

    return result


def find_empty_positions(
    grid: tp.List[tp.List[str]],
) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """

    for row_number, row in enumerate(grid):

        for column_number, value in enumerate(row):
            if value == ".":
                return (row_number, column_number)
    return None


def find_possible_values(
    grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """

    taken_values = list()
    taken_values = taken_values + get_block(grid, pos)
    taken_values = taken_values + get_row(grid, pos)
    taken_values = taken_values + get_col(grid, pos)

    taken_values = set(taken_values)

    all_values = "123456789"

    return set([value for value in all_values if value not in taken_values])


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """

    empty_spot = find_empty_positions(grid)

    if not empty_spot:
        return grid

    possible_values = find_possible_values(grid, empty_spot)

    if not possible_values:
        return None

    for value in possible_values:

        grid[empty_spot[0]][empty_spot[1]] = value
        if solve(grid):
            return solve(grid)
        else:
            grid[empty_spot[0]][empty_spot[1]] = "."

    return False


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles

    for row_number, row in enumerate(solution):

        if len(row) != len(set(row)):
            return False
        if "." in row:
            return False

        column = get_col(solution, (0, row_number))

        if len(column) != len(set(column)):
            return False
        if "." in column:
            return False

    for x in range(0, 9, 3):

        for y in range(0, 9, 3):
            block = get_block(solution, (x, y))
            if len(block) != len(set(block)):
                return False
            if "." in block:
                return False

    return True


def create_solved_gird():

    grid = list()

    first_row = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    shuffle(first_row)
    grid.append(first_row)

    prev = first_row
    for row_number in range(1, 9):

        if row_number == 3 or row_number == 6:

            new_indexes = [1, 2, 3, 4, 5, 6, 7, 8, 0]

            new_row = [i for i in range(9)]
            for index, new_index in enumerate(new_indexes):

                new_row[index] = prev[new_index]

        else:

            new_row = prev[3:6] + prev[6:9] + prev[0:3]

        prev = new_row
        grid.append(new_row)

    return grid


def generate_sudoku(n: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    pass

    grid = create_solved_gird()

    marked = list()
    n = 81 - n
    if n > 81:
        return [["." for _ in range(9)] for _ in range(9)]

    while len(marked) < n:

        x, y = random.randrange(0, 9), random.randrange(0, 9)
        pos = (x, y)
        if pos not in marked:
            grid[pos[0]][pos[1]] = "."
            marked.append(pos)

    return grid
