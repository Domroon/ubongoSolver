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

PINK_PIECE = {
    "color": 
        (250, 50, 100),
    "form":
        [[0, 1],
         [0, 1],
         [0, 1],
         [1, 1]]
}


class Tile(pg.sprite.Sprite):
    def __init__(self, size, pos, color=(255, 255, 255), border=True):
        super().__init__()
        self.image = pg.Surface([size, size])
        if border:
            self.image.fill((0, 0, 0))
        else:
            self.image.fill(color)
        self.pos = pos
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


class PlayingPiece(pg.sprite.Sprite):
    def __init__(self, pos, tiles_params, background_transparent=True):
        super().__init__()
        self.width = len(tiles_params["form"][0]) * TILE_WIDTH
        self.height = len(tiles_params["form"]) * TILE_WIDTH
        self.background_transparent = background_transparent
        self.rotations_angle = 90
        self.rotations = 0
        self.image = pg.Surface([self.width, self.height], pg.SRCALPHA, 32)
        self.image.fill((0, 255, 0))
        self.pos = pos
        self.rect = self.image.get_rect(topleft=self.pos)
        self.tiles_params = tiles_params
        self.tiles = pg.sprite.Group()
        self.rotated_tiles = pg.sprite.Group()
        self._add_tiles()
        self._blit_tiles()

    def _rotate_tiles(self):
        rotated_tiles = []
        col_num = len(self.tiles_params["form"][0])
        row_num = len(self.tiles_params["form"])
        for col in range(col_num):
            tiles_row = []
            for row in range(row_num, 0, -1):
                tiles_row.append(self.tiles_params["form"][row-1][col])
            rotated_tiles.append(tiles_row)
        self.tiles_params["form"].clear()
        self.tiles_params["form"] = rotated_tiles   

    def _add_tiles(self):
        for row_num in range(len(self.tiles_params["form"])):
            for col_num, col in enumerate(self.tiles_params["form"][row_num]):
                if col:
                    tile = Tile(
                        TILE_WIDTH, 
                        (col_num*TILE_WIDTH, row_num*TILE_WIDTH),
                        border=False,
                        color=self.tiles_params["color"]
                    )
                    self.tiles.add(tile)
    
    def _blit_tiles(self):
        for tile in self.tiles:
            self.image.blit(tile.image, tile.rect)

    def flip(self):
        # save first col
        first_col = []
        row_num = len(self.tiles_params["form"])
        for row in range(row_num):
            col_value = self.tiles_params["form"][row][0]
            first_col.append(col_value)
        
        # save values from the second row in the first row
        for row in range(row_num):
            col_value = self.tiles_params["form"][row][1]
            self.tiles_params["form"][row][0] = col_value
        
        # save values from the first row in the second row
        for row, value in enumerate(first_col):
            print("row", row)
            print("value", value)
            self.tiles_params["form"][row][1] = value
        print(self.tiles_params["form"])

        self.tiles.empty()
        self._add_tiles()
        self._blit_tiles()

    def rotate(self):
        self.rect = self.image.get_rect(topleft=self.pos)
        self.image = pg.transform.rotate(self.image, self.rotations_angle)
        
        self.tiles.empty()
        self._rotate_tiles()
        self._add_tiles()
        self._blit_tiles()
        for tile in self.tiles:
            tile.image = pg.transform.rotate(tile.image, self.rotations_angle)
            tile.rect = tile.image.get_rect(topleft=tile.pos)
            self.rotated_tiles.add(tile)
        self.tiles.empty()
        for tile in self.rotated_tiles:
            self.tiles.add(tile)
        self.rotated_tiles.empty()
        
    def update(self):
        empty = pg.Color(0,0,0,0)
        if self.background_transparent:
            self.image.fill(empty)
        else:
            self.image.fill((0, 255, 0))
        self._blit_tiles()


def main():
    pg.init()

    window = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Ubongo Solver")

    game_board = GameBoard(0, 0, GAME_BOARD_1)
    # tile = Tile(TILE_WIDTH, (10, 10))
    # tiles_group = pg.sprite.Group()
    # tiles_group.add(tile)
    piece = PlayingPiece((0, 0), PINK_PIECE)
    playing_pieces_group = pg.sprite.Group()
    playing_pieces_group.add(piece)

    piece.flip()
    
    clock = pg.time.Clock()
    fps = 1

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        window.fill((255, 100, 100))

        game_board.draw(window)
        
        piece.rotate()

        playing_pieces_group.update()
        playing_pieces_group.draw(window)
        
        # tiles_group.draw(window)
       
        
        pg.display.flip()

        clock.tick(fps)


if __name__ == '__main__':
    main()