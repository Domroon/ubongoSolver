import time
from random import shuffle

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
    "flippable": True,
    "rotatable": True
}

GREEN_PIECE = {
    "color": 
        (50, 255, 50),
    "form":
        [[1, 1],
         [1, 0]],
    "flippable": False,
    "rotatable": True
}

RED_PIECE = {
    "color": 
        (250, 50, 50),
    "form":
        [[1, 1],
         [1, 1]],
    "flippable": False,
    "rotatable": False
}

BLUE_PIECE = {
    "color": 
        (50, 50, 255),
    "form":
        [[1],
         [1],
         [1]],
    "flippable": False,
    "rotatable": True
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
        self.positions = []
        self.suitable_positions = []
        self.solution_position = None
        self.form = tiles_params["form"].copy()
        self.form_backup = tiles_params["form"].copy()
        self.color = tiles_params["color"]
        self.flippable = tiles_params["flippable"]
        self.flipped = False
        self.rotatable = tiles_params["rotatable"]
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

    def draw(self, window):
        self.tiles.draw(window)

    def rotate(self, clockwise=True):
        if clockwise:
            if self.rotatable:
                rotated_tiles = []
                # print("self form", self.form)
                # print("-------------------")
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
        else:
            for i in range(3):
                if self.rotatable:
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
                    self.tiles.empty()
                    self._add_tiles()
            self.rotations -= 1

    def flip(self):
        # self.reset()
        # save first col
        first_col = []
        row_num = len(self.form)
        for row in range(row_num):
            col_value = self.form[row][0]
            first_col.append(col_value)
            
        # save values from the second col in the first col
        for row in range(row_num):
            col_value = self.form[row][row_num - 3]
            self.form[row][0] = col_value
            
        # save values from the first col in the second col
        for row, value in enumerate(first_col):
            self.form[row][row_num - 3] = value
            
        self.tiles.empty()
        self._add_tiles()
        if not self.flipped:
            self.flipped = True
        else:
            self.flipped = False

    def change_pos(self, pos):
        self.x = pos["pos"][0]
        self.y = pos["pos"][1]
        self.tiles.empty()
        self._add_tiles()

        while True:
            if self.rotations == pos["rotations"]:
                break
            if self.rotations < pos["rotations"]:
                self.rotate()
            elif self.rotations > pos["rotations"]:
                    self.rotate(clockwise=False)

        if pos["flipped"] and not self.flipped and self.flippable:
            self.flip()
        if not pos["flipped"] and self.flipped and self.flippable:
            self.flip()

    def reset_pos(self):
        self.x = 0
        self.y = 0
        self.tiles.empty()
        self._add_tiles()

        while True:
            if self.rotations == 0:
                break
            if self.rotations < 0:
                self.rotate()
            elif self.rotations > 0:
                    self.rotate(clockwise=False)

        if self.flipped:
            self.flip()

    def reset(self):
        self.flipped = False
        self.rotations = 0
        self.x = 0
        self.y = 0
        self.tiles.empty()
        self.form.clear()
        self.form = self.form_backup
        self._add_tiles()


class Solver:
    def __init__(self, game_board, playing_pieces):
        self.game_board = game_board
        self.playing_pieces = playing_pieces
        self.suitable_positions = []
        self.solved_pieces = []

    def _check_completely_in_field(self, piece):
        for tile in piece.tiles:
            collides = pg.sprite.spritecollide(tile, self.game_board.tiles, False)
            if not collides:
                return False
        return True

    def _store_suitable_position(self, piece):
        pos_data = {
            "pos": [piece.x, piece.y],
            "rotations": piece.rotations,
            "flipped": piece.flipped
        }
        piece.suitable_positions.append(pos_data)

    # def _store_solution_position(self, piece):
    #     pos_data = {
    #         "pos": [piece.x, piece.y],
    #         "rotations": piece.rotations,
    #         "flipped": piece.flipped
    #     }
    #     piece.solution_position = pos_data
    
    # def _store_position(self, piece):
    #     pos_data = {
    #         "pos": [piece.x, piece.y],
    #         "rotations": piece.rotations,
    #         "flipped": piece.flipped
    #     }
    #     piece.positions.append(pos_data)

    def detect_suitable_positions(self, piece):
        print(f'Detect suitable positions for piece with color {piece.color}')
        while True:
            for tile in self.game_board.tiles.sprites():
                # piece.change_pos(tile.pos[0], tile.pos[1])
                piece.x = tile.pos[0]
                piece.y = tile.pos[1]
                piece.tiles.empty()
                piece._add_tiles()
                for i in range(4):
                    piece.rotate()
                    # self._store_position(piece)
                    if self._check_completely_in_field(piece):
                        self._store_suitable_position(piece)
            if piece.flipped or not piece.flippable:
                break
            if piece.flippable:
                piece.flip()
        # reset flip
        if piece.flippable:
            piece.flip()
 
    def _check_piece_overlapping(self, piece):
        # does any tile from the piece overlaps any tiles from all the other pieces?
        collide_counter = 0
        other_pieces = self.playing_pieces.copy()
        other_pieces.remove(piece)
        for tile in piece.tiles.sprites():
            # print(f'-->{tile.pos}')
            for other_piece in other_pieces:
                collide_list = pg.sprite.spritecollide(tile, other_piece.tiles, False)
                # print("collidelist", collide_list)
                for tile in collide_list:
                    # print(f'collide: {tile.pos}')
                    collide_counter += 1
        #     print("----------")
        # print("collide counter", collide_counter)
        if collide_counter > 0:
            return True
        else:
            return False

    def _try_every_piece(self):
        piece_num = 0
        while True:
            # 1 get a suitable pos from the piece and delete this pos from the piece
            if not self.playing_pieces:
                break
            try:
                piece = self.playing_pieces[piece_num]
            except IndexError:
                for piece in self.playing_pieces:
                    self.solved_pieces.append(piece)
                # print(self.solved_pieces)
                break
            if not piece.suitable_positions:
                self._store_solution_position(piece)
                self.solved_pieces.append(piece)
                self.playing_pieces.remove(piece)
                # piece_num -= 1
                continue
            piece_pos = piece.suitable_positions.pop()
            piece.change_pos(piece_pos["pos"][0], piece_pos["pos"][1])
            while True:
                if piece.rotations == piece_pos["rotations"]:
                    break
                if piece.rotations < piece_pos["rotations"]:
                    piece.rotate()
                elif piece.rotations > piece_pos["rotations"]:
                    piece.rotate(clockwise=False)
            if piece_pos["flipped"] and not piece.flipped and piece.flippable:
                piece.flip()
            if not piece_pos["flipped"] and piece.flipped and piece.flippable:
                piece.flip()
            
            # 2 check for overlaps with other pieces
            overlaps = self._check_piece_overlapping(piece)
            
            # overlaps ->true
            if overlaps:
                piece_num -= 1
                piece.change_pos(0, 0)
                continue
            # overlaps ->false
            if not overlaps:
                piece_num += 1
            for piece in self.playing_pieces:
                self._store_solution_position(piece)
        
    def solve(self, piece_num):
        try:
            piece = self.playing_pieces[piece_num]
            # store actual position here for show later?
        except IndexError:
            print("solved")

        if piece_num == 4:
            return True
        else:
            piece_num += 1

        
        positions = piece.suitable_positions
        shuffle(positions)
        for pos in positions:
            piece.change_pos(pos)
            overlapping = self._check_piece_overlapping(piece)

            if not overlapping:

                if self.solve(piece_num):
                    return True
            
            piece.reset_pos()
    
        return False


def main():
    pg.init()

    window = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Ubongo Solver")

    game_board = GameBoard(400, 150, GAME_BOARD_1)

    pink_piece = PlayingPiece(0, 0, PINK_PIECE)
    green_piece = PlayingPiece(0, 0, GREEN_PIECE)
    red_piece = PlayingPiece(0, 0, RED_PIECE)
    blue_piece = PlayingPiece(0, 0, BLUE_PIECE)

    playing_pieces = [pink_piece, green_piece, red_piece, blue_piece]

    solver = Solver(game_board, playing_pieces)
    for piece in solver.playing_pieces:
        solver.detect_suitable_positions(piece)
    # reset all pieces
    for piece in solver.playing_pieces:
        piece.reset_pos()
    
    print("Start solving Algorithm")
    solver.solve(0)

    


    clock = pg.time.Clock()
    fps = 20

    piece_num = 0
    pos_num = 0
    # max_pieces = len(playing_pieces)

    show_all_positions = False 
    show_suitable_positions = True
    show_solution = False


    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        window.fill((255, 100, 100))

        # if show_suitable_positions:
        #     fps = 3
        #     piece = playing_pieces[piece_num]
        #     piece.change_pos(piece.suitable_positions[pos_num])
        #     pos_num += 1
        #     if pos_num >= len(piece.suitable_positions):
        #         piece.reset_pos()
        #         piece_num += 1
        #         pos_num = 0

        game_board.draw(window)
        for piece in solver.playing_pieces:
            piece.draw(window)
       

        pg.display.flip()
        clock.tick(fps)

if __name__ == '__main__':
    main()