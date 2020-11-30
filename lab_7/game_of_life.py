import argparse

from util.game_logic import GameOfLife
from util.gui import GUI
from util.console import Console

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gui", help="Initialize GUI version of the game.")
    parser.add_argument(
        "--file",
        help="Path to file. Read the grid from file. Size arguments will be ignored.",
    )
    parser.add_argument(
        "--size",
        help="Input grid size in format: X-Y or just X if it's a rectangle. Default 50-50",
        default="8-8",
    )
    parser.add_argument(
        "--max",
        help="Input the number of maximum generations. Default 100",
        type=int,
        default=100,
    )
    parser.add_argument(
        "--cell_size",
        help="Input cell size. Only for GUI version. Default 50",
        type=int,
        default=50,
    )

    args = parser.parse_args()

    if args.file:
        life = GameOfLife.from_file(args.file, args.max)
    else:
        grid_size = (int(args.size.split("-")[0]), int(args.size.split("-")[1]))
        life = GameOfLife(
            size=grid_size,
            randomize=True,
            max_generations=args.max,
            cell_size=args.cell_size,
        )

    if args.gui:
        ui = GUI(life)
    else:
        ui = Console(life)

    ui.run()


if __name__ == "__main__":
    main()
