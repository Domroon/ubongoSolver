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
         [1, 1]],
    "flippable": True
}

GREEN_PIECE = {
    "color": 
        (50, 255, 50),
    "form":
        [[1, 1],
         [1, 0]],
    "flippable": True
}

RED_PIECE = {
    "color": 
        (250, 50, 50),
    "form":
        [[1, 1],
         [1, 1]],
    "flippable": False
}

BLUE_PIECE = {
    "color": 
        (50, 50, 255),
    "form":
        [[1],
         [1],
         [1]],
    "flippable": False
}

suitable_positions = []


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


class PlayingPiece:
    def __init__(self, x, y, tiles_params):
        self.x = x
        self.y = y
        self.form = tiles_params["form"]
        self.color = tiles_params["color"]
        self.flippable = tiles_params["flippable"]
        self.rotations = 0
        self.tiles = pg.sprite.Group()
        self._add_tiles()

    def _add_tiles(self):
        for row_num in range(len(self.form)):
            for col_num, col in enumerate(self.form[row_num]):
                if col:
                    tile = Tile(
                        TILE_WIDTH, 
                        (self.x + col_num*TILE_WIDTH, self.y + row_num*TILE_WIDTH),
                        border=True,
                        color=self.color
                    )
                    self.tiles.add(tile)

    def update(self):
        pass

    def draw(self, window):
        self.tiles.draw(window)

    def rotate(self):
        rotated_tiles = []
        col_num = len(self.form[0])
        row_num = len(self.form)
        for col in range(col_num):
            tiles_row = []
            for row in range(row_num, 0, -1):
                tiles_row.append(self.form[row-1][col])
            rotated_tiles.append(tiles_row)
        self.form.clear()
        self.form = rotated_tiles  
        self.rotations += 1
        self.tiles.empty()
        self._add_tiles()
        # print("rotated", self.rotations)

    def flip(self):
        if self.flippable:
            # save first col
            first_col = []
            row_num = len(self.form)
            for row in range(row_num):
                col_value = self.form[row][0]
                first_col.append(col_value)
            
            # save values from the second row in the first row
            for row in range(row_num):
                col_value = self.form[row][1]
                self.form[row][0] = col_value
            
            # save values from the first row in the second row
            for row, value in enumerate(first_col):
                self.form[row][1] = value
            
            self.tiles.empty()
            self._add_tiles()
            return True
        else:
            return False

    def change_pos(self, x, y):
        self.tiles.empty()
        self.x = x
        self.y = y
        self._add_tiles()





# Algorithm Steps

# # Step 1
# def find_suitable_positions(game_board, playing_piece, game_board_pos_num, active=True):
#     if active:
#         tile = game_board.tiles.sprites()[game_board_pos_num]
#         playing_piece.pos = tile.pos
class Solver:
    def __init__(self, game_board, playing_piece):
        self.game_board = game_board
        self.playing_piece = playing_piece

    def fits_in_the_field(self):
        for tile_num in range(len(self.playing_piece.tiles.sprites())):
            playing_piece_tile = self.playing_piece.tiles.sprites()[tile_num]
            collided = pg.sprite.spritecollide(playing_piece_tile, self.game_board.tiles, False)
            if not collided:
                return False
        return True
        print(collided)
        print("one piece tile: ", one_piece_sprite.pos)
        # for tile in self.game_board.tiles.sprites():
        #     print("game board pos: ", tile.pos)

    # oben links wird eine kollision erkannt
    # und laut print "one piece tile" befindet 
    # sich das tile auch an dieser stelle, obwohl es garnicht
    # dort ist
    # in PlayingPiece._add_tiles() habe ich nun pos addiert 
    # laut "one piece tile" befindet sich das tile nun an der richtigen
    # stelle, jedoch wird dieses nicht an der richtigen stelle
    # angezeigt, prüfe das bitte!!!
    # _blit_tiles eventuell fehlerhaft??


    # def find_suitable_positions(self):
    #     for tile in self.game_board.tiles.sprites():
    #         self.playing_piece.pos = tile.pos
    #         self.playing_piece.update()
    #         # collided = pg.sprite.collide_rect(tile, playing_piece)
    #         # print(tile.pos, collided)
            
    #         # für jedes sprite(tile) des pieces schauen ob
    #         # es mit einem sprite vom game board kollidiert ist
    #         for piece_tile in self.playing_piece.tiles.sprites():
    #             print(pg.sprite.spritecollide(piece_tile, self.game_board.tiles, False))
    #         print(self.game_board.tiles)
    #     print(pg.sprite.spritecollide(piece_tile, self.game_board.tiles, False))


recorded_steps = [
    # {"pos": [0, 0], "rotate": False, "flip": False},
    # {"pos": [50, 0], "rotate": False, "flip": False},
    # {"pos": [100, 0], "rotate": False, "flip": False},
    # {"pos": [200, 200], "rotate": False, "flip": False},
    # {"pos": [0, 0], "rotate": True, "flip": False},
    # {"pos": [0, 0], "rotate": True, "flip": False},
    # {"pos": [0, 0], "rotate": True, "flip": False},
    
    {"pos": [0, 0], "rotate": False, "flip": False},
    {"pos": [0, 0], "rotate": True, "flip": False},
    {"pos": [0, 0], "rotate": True, "flip": False},
    {"pos": [0, 0], "rotate": True, "flip": False},
    {"pos": [0, 0], "rotate": True, "flip": False},
    {"pos": [0, 0], "rotate": False, "flip": True},
    {"pos": [0, 0], "rotate": True, "flip": False},
    {"pos": [0, 0], "rotate": True, "flip": False},
    {"pos": [0, 0], "rotate": True, "flip": False},
    {"pos": [0, 0], "rotate": True, "flip": False},
]

def main():
    pg.init()

    window = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Ubongo Solver")

    # x=400 y=150
    game_board = GameBoard(0, 0, GAME_BOARD_1)
    piece = PlayingPiece(0, 0, PINK_PIECE)
    piece.change_pos(100, 0)
    piece.rotate()
    # piece.change_pos(500, 200)
    solver = Solver(game_board, piece)
    if solver.fits_in_the_field():
        print("Fits in the field")
    else:
        print("Fits NOT in the field")

    clock = pg.time.Clock()
    fps = 60

    step = 0

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        window.fill((255, 100, 100))

        # # execute saved solver steps
        # if step < len(recorded_steps):
        #     piece.change_pos(recorded_steps[step]["pos"][0], recorded_steps[step]["pos"][1])
        #     if recorded_steps[step]["rotate"]:
        #         piece.rotate()
        #     if recorded_steps[step]["flip"]:
        #         piece.flip()
        # step += 1

        game_board.draw(window)
        piece.draw(window)
        # playing_pieces_group.update()
        # playing_pieces_group.draw(window)
        pg.display.flip()
        clock.tick(fps)

if __name__ == '__main__':
    main()