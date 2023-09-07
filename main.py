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
    def __init__(self, playing_pieces):
        self.playing_pieces = playing_pieces
        self.recorded_steps = []
    
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
        # for data in self.suitable_positions:
        #     current_piece = None
        #     for piece in self.playing_pieces:
        #         if data["id"] == id(piece):
        #             current_piece = piece
        #     for pos in data["positions"]:
        #         current_piece.change_pos(pos["pos"][0], pos["pos"][1])
        #         current_piece.set_rotation_angle(pos["rotation_angle"])
        #         if pos["flipped"]:
        #             if current_piece.flipped:
        #                 pass
        #             else:
        #                 current_piece.flip()
        #         if not pos["flipped"]:
        #             if current_piece.flipped:
        #                 current_piece.flip()
        #             else:
        #                 pass
        #         self.recorder.add_step(current_piece, "Fits in the Field")

    def solve(self):
        for piece in self.playing_pieces:
            self._store_suitable_positions(piece)              
            

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
    
    # piece.change_pos(100, 0)
    # piece.rotate()
    # piece.change_pos(500, 200)

    game_board = GameBoard(400, 150, GAME_BOARD_1)

    pink_piece = PlayingPiece(0, 0, PINK_PIECE)
    green_piece = PlayingPiece(0, 0, GREEN_PIECE)
    red_piece = PlayingPiece(0, 0, GREEN_PIECE)
    blue_piece = PlayingPiece(0, 0, GREEN_PIECE)
    # [pink_piece, green_piece, red_piece, blue_piece]
    playing_pieces = [pink_piece, green_piece]
    recorder = StepRecorder(playing_pieces)
    solver = Solver(game_board, playing_pieces, recorder)
    solver.solve()
    for step in recorder.recorded_steps:
        print(step)

    # reset pieces before showing the recorded steps
    for piece in solver.playing_pieces:
        piece.change_pos(0, 0)

    clock = pg.time.Clock()
    fps = 30

    step = 0
    show_fitting_positions = False

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        window.fill((255, 100, 100))

        if show_fitting_positions:
            if recorder.recorded_steps[step]["fits_in_the_field"]:
                recorder.execute_stored_step(step)
        
        if not step > len(recorder.recorded_steps) - 2 and not show_fitting_positions:
            recorder.execute_stored_step(step)
            step += 1
        if not show_fitting_positions and step > len(recorder.recorded_steps) - 2:
            show_fitting_positions = True
            step = 0
        if show_fitting_positions and step > len(recorder.recorded_steps) - 2:
            break
        if not step > len(recorder.recorded_steps) - 2:
            step += 1
        game_board.draw(window)
        for piece in solver.playing_pieces:
            piece.draw(window)

        pg.display.flip()
        clock.tick(fps)

if __name__ == '__main__':
    main()