import time
from random import randint

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
    "flippable": True,
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
        [[0, 1],
         [0, 1],
         [0, 1]],
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
        self.form = tiles_params["form"]
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

    def update(self):
        pass

    def draw(self, window):
        self.tiles.draw(window)

    def rotate(self):
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
            self.rotations += 1
            self.tiles.empty()
            self._add_tiles()
    
    def set_rotation_angle(self, angle):
        if angle == 0:
            while True:
                if self.rotations == 0:
                    break
                if self.rotations == 4:
                    self.rotations = 0
                    break
                self.rotate()
        elif angle == 90:
            while True:
                if self.rotations == 1:
                    break
                if self.rotations == 4:
                    self.rotations = 0
                self.rotate()
        elif angle == 180:
            while True:
                if self.rotations == 2:
                    break
                if self.rotations == 4:
                    self.rotations = 0
                self.rotate()
        elif angle == 270:
            while True:
                if self.rotations == 3:
                    break
                if self.rotations == 4:
                    self.rotations = 0
                self.rotate()

    def get_rotation_angle(self):
        if self.rotations == 0:
            return 0
        elif self.rotations == 1:
            return 90
        elif self.rotations == 2:
            return 180
        elif self.rotations == 3:
            return 270
        elif self.rotations == 4:
            return 0

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
            if not self.flipped:
                self.flipped = True
            else:
                self.flipped = False
            return True
        else:
            return False

    def change_pos(self, x, y):
        self.tiles.empty()
        self.x = x
        self.y = y
        self._add_tiles()


class StepRecorder:
    def __init__(self, playing_pieces, print_info_text=True):
        self.playing_pieces = playing_pieces
        self.recorded_steps = []
        self.print_info_text = print_info_text
    
    def add_step(self, piece, info_text, fits=False):
        step = {
            "piece_id": id(piece),
            "pos": [piece.x, piece.y],
            "rotation_angle": piece.get_rotation_angle(),
            "flipped": piece.flipped,
            "info_text": info_text,
            "fits_in_the_field": fits
        }
        self.recorded_steps.append(step)

    def execute_stored_step(self, step):
        current_step = self.recorded_steps[step]
        current_piece = None
        for piece in self.playing_pieces:
            if id(piece) == current_step["piece_id"]:
                current_piece = piece
        current_piece.change_pos(current_step["pos"][0], current_step["pos"][1])
        current_piece.set_rotation_angle(current_step["rotation_angle"])
        if current_step["flipped"]:
            if current_piece.flipped:
                pass
            else:
                current_piece.flip()
        else:
            if current_piece.flipped:
                current_piece.flip()
            else:
                pass
        
        if self.print_info_text:
            print(current_step["info_text"])
    

class Solver:
    def __init__(self, game_board, playing_pieces, step_recorder):
        self.game_board = game_board
        self.playing_pieces = playing_pieces
        self.recorder = step_recorder
        self.suitable_positions = []

    def _fits_in_the_field(self, piece):
        for tile_num in range(len(piece.tiles.sprites())):
            playing_piece_tile = piece.tiles.sprites()[tile_num]
            collided = pg.sprite.spritecollide(playing_piece_tile, self.game_board.tiles, False)
            if not collided:
                return False
        return True

    def _store_suitable_positions(self, piece):
        positions = []
        while True:
            if piece.rotations > 3 and not piece.flipped:
                piece.rotations = 0
                if not piece.flippable:
                    break
                piece.flip()
            elif piece.rotations > 3 and piece.flipped:
                piece.rotations = 0
                break
            for tile in self.game_board.tiles.sprites():
                piece.change_pos(tile.pos[0], tile.pos[1])
                self.recorder.add_step(piece, "Possible Position")
                if self._fits_in_the_field(piece):
                    self.recorder.add_step(piece, "Fits in the Field", fits=True)
                    positions.append({
                        "pos": [piece.x, piece.y],
                        "rotation_angle": piece.get_rotation_angle(),
                        "flipped": piece.flipped
                        })
            if not piece.rotatable:
                break
            piece.rotate()
        data = {
            "id": id(piece),
            "color": piece.color,
            "positions": positions
        }
        self.suitable_positions.append(data)

    # def _delete_suitable_pos(self, piece_id, pos_list_num):
    #     for suit_pos in self.suitable_positions:
    #         if suit_pos["id"] == piece_id:
    #             piece_suitable_positions = suit_pos["positions"]
    #     piece_suitable_positions.remove

    def _get_random_suitable_position_data(self, piece):
        # piece_suitable_positions = []
        piece_id = id(piece)
        for suit_pos in self.suitable_positions:
            if suit_pos["id"] == piece_id:
                if not suit_pos["positions"]:
                    return False
                else:
                    random_list_num = randint(0, len(suit_pos["positions"])-1)
                    print("len", len(suit_pos["positions"]))
                    piece_suitable_position = suit_pos["positions"].pop(random_list_num)
        
                    return piece_suitable_position
        
        # random_list_num = randint(0, len(piece_suitable_positions))
        # cached_suitable_pos = piece_suitable_positions[random_list_num]
        # self._delete_suitable_pos(piece_id, random_list_num)
        # print(cached_suitable_pos)

    def solve(self):
        # 0 find suitable positions for every playing piece
        for piece in self.playing_pieces:
            self._store_suitable_positions(piece)

        piece_num = 0
        # 1 take a piece and put it to a suitable position, remove this pos from suitable_pos
        # get a suitable positions for the given piece
        piece = self.playing_pieces[piece_num]
        rand_pos = self._get_random_suitable_position_data(piece)
        self.playing_pieces[piece_num].change_pos(rand_pos['pos'][0], rand_pos['pos'][1])
        self.playing_pieces[piece_num].set_rotation_angle(rand_pos['rotation_angle'])
        if rand_pos["flipped"]:
            if piece.flipped:
                pass
            else:
                piece.flip()
        if not rand_pos["flipped"]:
            if piece.flipped:
                piece.flip()
            else:
                pass
        self.recorder.add_step(piece, info_text=f'Try this position: \nexpected: {rand_pos}\nreal value: pos: [{piece.x},{piece.y}], rotation_angle: {piece.get_rotation_angle()}, flipped: {piece.flipped}')


        # 2 does this piece fit without overlapping an other piece?
            # yes -> 2.1 is there another piece (with a position not tested) to put on game board? 
            #           -> yes: goto 1
            #           -> no: solved

        # 3 put the piece from before to another position
        
        # 4 is there a position that is not set before for this piece?
            # no -> go to 3
            # yes -> goto 2.1     
            

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

    game_board = GameBoard(400, 150, GAME_BOARD_1)

    pink_piece = PlayingPiece(0, 0, PINK_PIECE)
    green_piece = PlayingPiece(0, 0, GREEN_PIECE)
    red_piece = PlayingPiece(0, 0, RED_PIECE)
    blue_piece = PlayingPiece(0, 0, BLUE_PIECE)

    playing_pieces = [pink_piece, green_piece, red_piece, blue_piece]

    recorder = StepRecorder(playing_pieces, print_info_text=True)
    solver = Solver(game_board, playing_pieces, recorder)
    solver.solve()
    for step in recorder.recorded_steps:
        print(step)

    # reset pieces before showing the recorded steps
    for piece in solver.playing_pieces:
        piece.change_pos(0, 0)

    clock = pg.time.Clock()
    fps = 120

    step = 0
    show_fitting_positions = False

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        window.fill((255, 100, 100))

        # if show_fitting_positions:
        #     if recorder.recorded_steps[step]["fits_in_the_field"]:
        #         recorder.execute_stored_step(step)
        
        # if not step > len(recorder.recorded_steps) - 2 and not show_fitting_positions:
        #     recorder.execute_stored_step(step)
        #     step += 1
        # if not show_fitting_positions and step > len(recorder.recorded_steps) - 2:
        #     show_fitting_positions = True
        #     step = 0
        # if step == len(recorder.recorded_steps) - 2:
        #     recorder.execute_stored_step(step)
        # if show_fitting_positions and step > len(recorder.recorded_steps) - 2:
        #     pass
        # if not step > len(recorder.recorded_steps) - 2:
        #     step += 1
        if not step > len(recorder.recorded_steps) - 1:
            recorder.execute_stored_step(step)
            step += 1

        game_board.draw(window)
        for piece in solver.playing_pieces:
            piece.draw(window)

        pg.display.flip()
        clock.tick(fps)

if __name__ == '__main__':
    main()