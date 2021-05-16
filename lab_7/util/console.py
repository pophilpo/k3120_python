import curses

from util.ui import UI


class Console(UI):
    def __init__(self, life):
        super().__init__(life)

    def draw_borders(self, screen):

        begin_x = 0
        begin_y = 0

        # Adding plus 3 so that points don't cross borders
        height = self.life.rows + 3
        width = self.life.cols + 3

        grid = screen.subwin(height, width, begin_x, begin_y)

        grid.box()
        screen.getch()

    def draw_grid(self, screen):

        for x, row in enumerate(self.life.curr_grid):

            for y, value in enumerate(row):

                pos_x = x + 1
                pos_y = y + 1

                if value == 1:
                    screen.addch(pos_x, pos_y, "O")
                else:
                    screen.addch(pos_x, pos_y, ".")

        screen.refresh()

    def run(self):

        screen = curses.initscr()
        self.draw_borders(screen)

        self.draw_grid(screen)
        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            self.life.step()
            self.draw_grid(screen)
            curses.napms(self.life.speed)

        screen.getkey()
        curses.endwin()
