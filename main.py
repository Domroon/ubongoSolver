import pygame as pg


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

TILE_WIDTH = 100

GAME_BOARD_1 = [
    [1, 1, 1, 0],
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1]
]

GAME_BOARD_2 = [
    [1, 1, 0]
]

# class Tile:
#     def __init__(self, x, y, square_lengths, color=(255,255,255), border_thickness=4):
#         self.x = x
#         self.y = y
#         self.width = square_lengths
#         self.height = square_lengths
#         self.color = color
#         self.border_thickness = border_thickness

#     def draw(self, window):
#         pg.draw.rect(window, (0, 0, 0), (self.x, self.y, self.width, self.height))
#         pg.draw.rect(
#             window,
#             self.color, 
#             (self.x+self.border_thickness, 
#              self.y+self.border_thickness, 
#              self.width-self.border_thickness*2, 
#              self.height-self.border_thickness*2)
#         )

class Tile(Sprite):
    def __init__(self, size, pos, color=(255, 255, 255)):
        super().__init__()
        self.surface = pg.Surface(size)
        self.surface.fill((0, 0, 0))
        self.rect = self.surface.get_rect(center=pos)
        self.inner_surface = Surface([size/1.2, size/1.2])
        self.inner_surface.fill(color)
        self.inner_rect = self.inner_surface.get_rect(center=[size/2, size/2])
        self.surface.blit(self.inner_surface, self.inner_surface)
# test the tile class by adding it to a group and then print
# it to the screen!

# rewrite like in hitTheBlock! with the new tile class
# es müssen tiles hinzugefügt werden können
# diese müssen außerdem auf ein neues surface geschrieben
# werden damit dieses als ganzes rotiert werden kann!
# rotate surface https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
# flip image:  https://www.geeksforgeeks.org/pygame-flip-the-image/

class GameBoard:
    def __init__(self, x, y, board_rows):
        self.x = x
        self.y = y
        self.board_rows = board_rows
        self.tiles = []
        self._init_board_cols()

    def _init_board_cols(self):
        for row_num in range(len(self.board_rows)):
            tile_row = []
            for col_num, col in enumerate(self.board_rows[row_num]):
                if col:
                    tile = Tile(self.x + col_num*TILE_WIDTH, self.y + row_num*TILE_WIDTH, TILE_WIDTH)
                    tile_row.append(tile)
            self.tiles.append(tile_row)

    def draw(self, window):
        for row in self.tiles:
            for tile in row:
                tile.draw(window)


class PlayingPiece:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def main():
    pg.init()

    window = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Ubongo Solver")

    # game_board = GameBoard(100, 100, GAME_BOARD_1)
    
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        window.fill((255, 100, 100))
        game_board.draw(window)
        pg.display.flip()


if __name__ == '__main__':
    main()