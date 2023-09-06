import time

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


class Tile(pg.sprite.Sprite):
    def __init__(self, size, pos, color=(255, 255, 255)):
        super().__init__()
        self.image = pg.Surface([size, size])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect(topleft=pos)
        self.inner_image = pg.Surface([size/1.1, size/1.1])
        self.inner_image.fill(color)
        self.inner_rect = self.inner_image.get_rect(center=[size/2, size/2])
        self.image.blit(self.inner_image, self.inner_rect)


class GameBoard:
    def __init__(self, x, y, game_board_list):
        self.x = x
        self.y = y
        self.game_board_list = game_board_list
        self.tiles = pg.sprite.Group()
        self._init_board_cols()

    def _init_board_cols(self):
        for row_num in range(len(self.game_board_list)):
            for col_num, col in enumerate(self.game_board_list[row_num]):
                if col:
                    tile = Tile(TILE_WIDTH, (self.x + col_num*TILE_WIDTH, self.y + row_num*TILE_WIDTH))
                    self.tiles.add(tile)

    def draw(self, window):
        self.tiles.draw(window)

# write like in hitTheBlock! with the new tile class
# es müssen tiles hinzugefügt werden können
# diese müssen außerdem auf ein neues surface geschrieben
# werden damit dieses als ganzes rotiert werden kann!
# rotate surface https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
# flip image:  https://www.geeksforgeeks.org/pygame-flip-the-image/





def main():
    pg.init()

    window = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Ubongo Solver")

    game_board = GameBoard(0, 0, GAME_BOARD_1)
    # tile = Tile(TILE_WIDTH, (10, 10))
    # tiles_group = pg.sprite.Group()
    # tiles_group.add(tile)
    # piece = PlayingPiece((150, 150), [0, 0, 0])
    # playing_pieces_group = pg.sprite.Group()
    # playing_pieces_group.add(piece)
    
    clock = pg.time.Clock()
    fps = 1

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        window.fill((255, 100, 100))

        game_board.draw(window)
        
        # playing_pieces_group.update()
        # piece.rotate()
        # playing_pieces_group.draw(window)
        
        # tiles_group.draw(window)
        
        pg.display.flip()

        clock.tick(fps)


if __name__ == '__main__':
    main()