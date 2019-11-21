import pygame
from config import Cfg as cfg


class Area(pygame.Surface):
    def __init__(self, size, color, coords=None, parent=None):
        super().__init__(size=size)

        self.size = size
        self.width, self.height = self.size
        self.coords = coords
        self.parent = parent

        self.color = color
        self.fill(color)

        # attr is used by subclasses to assign the
        #   blit object in self.main_blit()
        self.blit_obj = self

    def refill(self, alt_color):
        self.fill(alt_color)

    @property
    def main_blit(self):
        return self.blit_obj, self.coords


class LifeSquare(Area):
    COLOR_DEAD = cfg.GRAY
    COLOR_ALIVE = cfg.AQUA

    def __init__(self, size, coords, parent, alive=False):
        super().__init__(size=size,
                         coords=coords,
                         color=self.COLOR_DEAD,
                         parent=parent)

        self.alive = alive
        if self.alive:
            self.color = self.COLOR_ALIVE
        else:
            self.color = self.COLOR_DEAD

        self.img_rect = self.get_rect(topleft=self.mouse_pos_offset_coords())

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f"<{cls_name}: coords={self.coords}, alive={self.alive}>"

    def update_square(self):
        if self.alive:
            self.convert_to_dead()
        else:
            self.convert_to_alive()

    def convert_to_dead(self):
        self.color = self.COLOR_DEAD
        self.alive = False
        self.refill(self.color)

    def convert_to_alive(self):
        self.color = self.COLOR_ALIVE
        self.alive = True
        self.refill(self.color)

    def mouse_pos_offset_coords(self):
        x, y = self.coords
        y += cfg.MENU_HEIGHT
        return (x, y)


class Board(Area):
    # TODO: this looks gross...
    SQ_DIM = 20
    SQ_PAD = 3
    FIN_DIM = SQ_DIM - SQ_PAD
    FIN_SIZE = FIN_DIM, FIN_DIM

    def __init__(self, size, coords=None, color=None):
        super().__init__(size=size, coords=coords, color=color)
        self.squares = self.create_board()
        self.update_blit()

    def create_board(self):
        # each range subtracts one square dimension to
        #   keep everything on the board
        x_range = range(0, (self.width - self.SQ_DIM), self.SQ_DIM)
        y_range = range(0, (self.height - self.SQ_DIM), self.SQ_DIM)

        squares = [[self.create_square(x, y) for y in y_range]
                   for x in x_range]

        return squares

    def create_square(self, x, y, alive=False):
        coords = (x + self.SQ_PAD, y + self.SQ_PAD)
        square = LifeSquare(size=self.FIN_SIZE,
                            coords=coords,
                            parent=self,
                            alive=alive)
        return square

    def clear_board(self):
        for _, square in self.square_gen():
            square.convert_to_dead()

    def update_blit(self):
        for _, square in self.square_gen():
            self.blit(square, square.coords)

    def run_sim(self):
        # TODO: live squares at the bottom of the board effect
        #           squares at the top...

        # Create a snapshot of alive values from the current board
        temp_squares = [[square.alive for square in row]
                        for row in self.squares]

        # using matrix-positional (x, y) coordinates
        for (x, y), square in self.square_gen():
            neighbor_count = 0
            # matrix-positional coordinates of neighbors
            for dx, dy in self.neighbor_pos_gen():
                try:
                    neighbor_alive = temp_squares[x + dx][y + dy]
                    neighbor_count += int(neighbor_alive)
                except IndexError:
                    continue

            # ------------- Conway's Game of Life Rule Set -------------
            if square.alive and (neighbor_count < 2 or neighbor_count > 3):
                square.convert_to_dead()
            elif not square.alive and neighbor_count == 3:
                square.convert_to_alive()

        self.update_blit()

    def square_gen(self):
        # TODO: vairables x & y are matrix positions not pygame coordinates...
        for x, row in enumerate(self.squares):
            for y, square in enumerate(row):
                yield (x, y), square

    @staticmethod
    def neighbor_pos_gen(dist=1):
        r = range(-dist, dist + 1)
        for dy in r:
            for dx in r:
                if dx == 0 and dy == 0:
                    continue
                else:
                    yield (dx, dy)


class MenuButton(Area):
    BTN_PAD = 25
    BTN_LEFT = 30

    def __init__(self, parent, img_loc, nth_pos):
        super().__init__(size=cfg.BTN_SIZE, color=cfg.TEAL, parent=parent)
        self.img_loc = img_loc
        self.img_name = self.img_loc.split('/')[-1].split('.')[0]
        self.img = pygame.image.load(self.img_loc)
        self.blit_obj = self.img

        self.nth_pos = nth_pos
        self.x = self.btn_spcr(self.nth_pos)
        self.y = self.vertical_center_in_parent()
        self.coords = (self.x, self.y)

        self.img_rect = self.img.get_rect(topleft=self.coords)
        self.bg = Area(size=self.size, coords=self.coords, color=self.color)

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f"<{cls_name}: {self.img_name}>"

    def vertical_center_in_parent(self):
        return (self.parent.height / 2) - (self.width / 2)

    def btn_spcr(self, nth_pos, pad=BTN_PAD, left=BTN_LEFT):
        return ((nth_pos - 1) * (32 + pad)) + left

    @property
    def bg_blit(self):
        return self.bg, self.coords


class BlitList:
    def __init__(self, objs=[]):
        self.objs = objs

    def update(self, target, new_obj, pre=True):
        i = self.objs.index(target)
        if pre:
            i -= 1
        self.objs.insert(i, new_obj)

    def remove(self, target):
        self.objs.remove(target)

    def replace(self, i, new_obj):
        self.objs[i] = new_obj

    def highlight_updater(self, btns, mouse_pos):
        for btn in btns:
            if btn.img_rect.collidepoint(mouse_pos):
                self.update(btn.main_blit, btn.bg_blit)
            else:
                try:
                    self.remove(btn.bg_blit)
                except ValueError:
                    continue
