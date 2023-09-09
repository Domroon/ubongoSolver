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

    def rotate(self, clockwise=False):
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
    
    # def set_rotation_angle(self, angle):
    #     if angle == 0:
    #         while True:
    #             if self.rotations == 0:
    #                 break
    #             if self.rotations == 4:
    #                 self.rotations = 0
    #                 break
    #             self.rotate()
    #     elif angle == 90:
    #         while True:
    #             if self.rotations == 1:
    #                 break
    #             if self.rotations == 4:
    #                 self.rotations = 0
    #             self.rotate()
    #     elif angle == 180:
    #         while True:
    #             if self.rotations == 2:
    #                 break
    #             if self.rotations == 4:
    #                 self.rotations = 0
    #             self.rotate()
    #     elif angle == 270:
    #         while True:
    #             if self.rotations == 3:
    #                 break
    #             if self.rotations == 4:
    #                 self.rotations = 0
    #             self.rotate()

    # def get_rotation_angle(self):
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

    def change_pos(self, x, y):
        self.x = x
        self.y = y
        self.tiles.empty()
        self._add_tiles()

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
    
    def _store_position(self, piece):
        pos_data = {
            "pos": [piece.x, piece.y],
            "rotations": piece.rotations,
            "flipped": piece.flipped
        }
        piece.positions.append(pos_data)

    def _move_to_every_bord_pos(self, piece):
        while True:
            for tile in self.game_board.tiles.sprites():
                piece.change_pos(tile.pos[0], tile.pos[1])
                for i in range(4):
                    piece.rotate()
                    self._store_position(piece)
                    if self._check_completely_in_field(piece):
                        self._store_suitable_position(piece)
            if piece.flipped:
                break
            piece.flip()
        # reset flip
        piece.flip()
 
    def solve(self):
        self._move_to_every_bord_pos(self.playing_pieces[0])
    

    

    # def _move_to_every_bord_pos(self, piece):
    #     while True:
    #         while True:
    #             if piece.rotations > 3:
    #                 piece.rotate()
    #                 piece.rotations = 0
    #                 break
    #             for tile in self.game_board.tiles:
    #                 piece.change_pos(tile.pos[0], tile.pos[1])
    #                 if self._check_completely_in_field(piece):
    #                     self._store_suitable_position(piece)
    #             if not piece.rotatable:
    #                 break
    #             piece.rotate()
    #         if not piece.flippable:
    #             break
    #         if piece.flipped:
    #             break
    #         piece.flip()

    # def _find_suitable_positions(self):
    #     for piece in self.playing_pieces:
    #         self._move_to_every_bord_pos(piece)
    
    # def _get_suitable_pos(self, piece, random=False):
    #     positions = piece.suitable_positions
    #     if not positions:
    #         return False
    #     if random:
    #         random_num = randint(0, len(positions)-1)
    #         return positions.pop(random_num)
    #     return positions.pop()

    # def _check_piece_overlapping(self, piece):
    #     # does any tile from the piece overlaps any tiles from all the other pieces?
    #     collide_counter = 0
    #     other_pieces = self.playing_pieces.copy()
    #     other_pieces.remove(piece)
    #     for tile in piece.tiles.sprites():
    #         # print(f'-->{tile.pos}')
    #         for other_piece in other_pieces:
    #             collide_list = pg.sprite.spritecollide(tile, other_piece.tiles, False)
    #             # print("collidelist", collide_list)
    #             for tile in collide_list:
    #                 # print(f'collide: {tile.pos}')
    #                 collide_counter += 1
    #     #     print("----------")
    #     # print("collide counter", collide_counter)
    #     if collide_counter > 0:
    #         return True
    #     else:
    #         return False

    # def solve(self):
        # self._find_suitable_positions()
        # for piece in self.playing_pieces:
        #     piece.reset()
        # for pos in self.playing_pieces[0].suitable_positions:
        #     print(pos)
        # piece_num = 0
        # while True:
        #     if piece_num > len(self.playing_pieces) - 1:
        #         break
        #     while True:
        #         piece = self.playing_pieces[piece_num]
        #         pos = self._get_suitable_pos(piece, random=True)
        #         # piece.reset()
        #         # print("suitable pos", pos)
        #         if not pos:
        #             break
        #         # pos_copy = self._get_suitable_pos(piece, random=True).copy()
        #         piece.change_pos(pos["pos"][0], pos["pos"][1])
        #         # print(piece.x, piece.y)
        #         if pos["flipped"]:
        #             piece.flip()
        #         for i in range(pos["rotations"]):
        #             piece.rotate()
        #         if self._check_piece_overlapping(piece):
        #             piece_num -= 1
        #             print(piece_num)
        #         # piece.reset()
        #     piece_num += 1
                                            


        # for piece in self.playing_pieces:
        #     for pos in piece.suitable_positions:
        #         print(pos)
        #     print("--------------------")
        #     piece.reset()


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

    # recorder = StepRecorder(playing_pieces, print_info_text=False)
    solver = Solver(game_board, playing_pieces)
    solver.solve()
    for pos in playing_pieces[0].suitable_positions:
        print(pos)
    # for pos in playing_pieces[0].suitable_positions:
    #     print(pos)
    # for step in recorder.recorded_steps:
    #     print(step)

    # reset pieces before showing the recorded steps
    # for piece in solver.playing_pieces:
    #     piece.change_pos(0, 0)

    clock = pg.time.Clock()
    fps = 5

    piece_num = 0
    pos_num = 0

    show_all_positions = True
    show_suitable_positions = False

    # for row in PINK_PIECE["form"]:
    #     print(row)
    # print(playing_pieces[0].flipped)

    # reset rotations 
    playing_pieces[piece_num].rotations = 0

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        window.fill((255, 100, 100))

        piece = playing_pieces[piece_num]
        # show all positions
        if show_all_positions:
            # piece = playing_pieces[piece_num]
            piece.change_pos(
                piece.positions[pos_num]["pos"][0],
                piece.positions[pos_num]["pos"][1]
            )
            piece.rotate()
            if piece.positions[pos_num]["flipped"] and not piece.flipped:
                piece.flip()
            if not piece.positions[pos_num]["flipped"] and piece.flipped:
                piece.flip()
            pos_num += 1
        if pos_num >= len(piece.positions):
            show_all_positions = False
            show_suitable_positions = True
            pos_num = 0
            piece.rotations = 0

        # show suitable positions
        if show_suitable_positions:
            fps = 1
            # piece = playing_pieces[piece_num]
            piece.change_pos(
                piece.suitable_positions[pos_num]["pos"][0],
                piece.suitable_positions[pos_num]["pos"][1]
            )
            while piece.rotations < piece.suitable_positions[pos_num]["rotations"]:
                piece.rotate()
            if piece.suitable_positions[pos_num]["flipped"] and not piece.flipped:
                piece.flip()
            if not piece.suitable_positions[pos_num]["flipped"] and piece.flipped:
                piece.flip()
            pos_num += 1
        if pos_num >= len(piece.suitable_positions):
            show_suitable_positions = False

        
        print("piece rotations", piece.rotations)
        print("fipped", piece.flipped)


        # show all suitable positions
        # playing_pieces[piece_num].reset()
        # playing_pieces[piece_num].change_pos(
        #     playing_pieces[piece_num].suitable_positions[pos_num]["pos"][0],
        #     playing_pieces[piece_num].suitable_positions[pos_num]["pos"][1]
        # )
        # print("rotations", playing_pieces[piece_num].suitable_positions[pos_num]["rotations"])
        # saved_rotations = playing_pieces[piece_num].suitable_positions[pos_num]["rotations"]
        # for i in range(0, saved_rotations):
        #     if playing_pieces[piece_num].rotations > 3:
        #         playing_pieces[piece_num].rotations = 0 
        #     if playing_pieces[piece_num].rotations < saved_rotations:
        #         playing_pieces[piece_num].rotate()
        # if not playing_pieces[piece_num].flipped and playing_pieces[piece_num].suitable_positions[pos_num]["flipped"]:
        #     playing_pieces[piece_num].flip()
           
        # pos_num += 1

        game_board.draw(window)
        for piece in solver.playing_pieces:
            piece.draw(window)
       

        pg.display.flip()
        clock.tick(fps)

if __name__ == '__main__':
    main()


# class StepRecorder:
#     def __init__(self, playing_pieces, print_info_text=True):
#         self.playing_pieces = playing_pieces
#         self.recorded_steps = []
#         self.print_info_text = print_info_text
    
#     def add_step(self, piece, info_text, fits=False):
#         step = {
#             "piece_id": id(piece),
#             "pos": [piece.x, piece.y],
#             "rotation_angle": piece.get_rotation_angle(),
#             "flipped": piece.flipped,
#             "info_text": info_text,
#             "fits_in_the_field": fits
#         }
#         self.recorded_steps.append(step)

#     def execute_stored_step(self, step):
#         current_step = self.recorded_steps[step]
#         current_piece = None
#         for piece in self.playing_pieces:
#             if id(piece) == current_step["piece_id"]:
#                 current_piece = piece
#         current_piece.change_pos(current_step["pos"][0], current_step["pos"][1])
#         current_piece.set_rotation_angle(current_step["rotation_angle"])
#         if current_step["flipped"]:
#             if current_piece.flipped:
#                 pass
#             else:
#                 current_piece.flip()
#         else:
#             if current_piece.flipped:
#                 current_piece.flip()
#             else:
#                 pass
        
#         if self.print_info_text:
#             print(current_step["info_text"])
    

## solver 
#    def _fits_in_the_field(self, piece):
#         for tile_num in range(len(piece.tiles.sprites())):
#             playing_piece_tile = piece.tiles.sprites()[tile_num]
#             collided = pg.sprite.spritecollide(playing_piece_tile, self.game_board.tiles, False)
#             if not collided:
#                 return False
#         return True

#     def _store_suitable_positions(self, piece):
#         positions = []
#         while True:
#             if piece.rotations > 3 and not piece.flipped:
#                 piece.rotations = 0
#                 if not piece.flippable:
#                     break
#                 piece.flip()
#                 piece.flipped = True
#             elif piece.rotations > 3 and piece.flipped:
#                 piece.rotations = 0
#                 break
#             for tile in self.game_board.tiles.sprites():
#                 piece.change_pos(tile.pos[0], tile.pos[1])
#                 # self.recorder.add_step(piece, "Possible Position")
#                 if self._fits_in_the_field(piece):
#                     # self.recorder.add_step(piece, "Fits in the Field", fits=True)
#                     positions.append({
#                         "pos": [piece.x, piece.y],
#                         "rotation_angle": piece.get_rotation_angle(),
#                         "rotations": piece.rotations,
#                         "flipped": piece.flipped
#                         })
#             if not piece.rotatable:
#                 break
#             piece.rotate()
#         data = {
#             "id": id(piece),
#             "color": piece.color,
#             "positions": positions
#         }
#         self.suitable_positions.append(data)

#     def _get_random_suitable_position_data(self, piece, random=True): # its not longer random!!
#         # piece_suitable_positions = []
#         piece_id = id(piece)
#         for suit_pos in self.suitable_positions:
#             if suit_pos["id"] == piece_id:
#                 if not suit_pos["positions"]:
#                     return False
#                 else:
#                     random_list_num = randint(0, len(suit_pos["positions"])-1)
#                     # print("len", len(suit_pos["positions"]))
#                     if random:
#                         piece_suitable_position = suit_pos["positions"].pop(random_list_num)
#                     else:
#                         piece_suitable_position = suit_pos["positions"].pop()
        
#                     return piece_suitable_position

#     def _add_piece_to_board(self, piece):
#         piece.reset()
#         rand_pos = self._get_random_suitable_position_data(piece, random=True)
#         if not rand_pos:
#             return False
#         piece.change_pos(rand_pos['pos'][0], rand_pos['pos'][1])
#         # piece.set_rotation_angle(rand_pos['rotation_angle'])
#         for rotation in range(rand_pos['rotations']):
#             piece.rotate()
#         if rand_pos["flipped"]:
#             if piece.flipped:
#                 pass
#             else:
#                 piece.flip()
#                 piece.flipped = True
#         if not rand_pos["flipped"]:
#             if piece.flipped:
#                 piece.flip()
#                 piece.flipped = False
#             else:
#                 pass
#         self.recorder.add_step(piece, info_text=f'Try this position: \nexpected: {rand_pos}\nreal value: pos: [{piece.x},{piece.y}], rotation_angle: {piece.get_rotation_angle()}, flipped: {piece.flipped}')
#         return True

#     def check_piece_overlapping(self, piece):
#         # does any tile from the piece overlaps any tiles from all the other pieces?
#         collide_counter = 0
#         other_pieces = self.playing_pieces.copy()
#         other_pieces.remove(piece)
#         for tile in piece.tiles.sprites():
#             # print(f'-->{tile.pos}')
#             for other_piece in other_pieces:
#                 collide_list = pg.sprite.spritecollide(tile, other_piece.tiles, False)
#                 # print("collidelist", collide_list)
#                 for tile in collide_list:
#                     # print(f'collide: {tile.pos}')
#                     collide_counter += 1
#         #     print("----------")
#         # print("collide counter", collide_counter)
#         if collide_counter > 0:
#             return True
#         else:
#             return False

#     def solve(self):
# def solve():
#         # 0 find suitable positions for every playing piece
#         for piece in self.playing_pieces:
#             self._store_suitable_positions(piece)
#             # for suit_pos in self.suitable_positions:
#             #     if suit_pos["id"] == id(piece):
#             #         for pos in suit_pos["positions"]:
#             #             print(pos)
#             #         print("----------------------------------")

#         # 0.1 reset piece postitions
#         for piece in self.playing_pieces:
#             piece.reset()
#             self.recorder.add_step(piece, "Reset all Piece positions")

#         # for piece in self.playing_pieces:
#         #     piece.change_pos(0, 0)
#         #     self.recorder.add_step(piece, "Reset all Piece positions")

#         pieces = self.playing_pieces.copy()
#         # 1 take a piece and put it to a suitable position, remove this pos from suitable_pos
#         piece_num = 0

#         while True:
#             if not pieces:
#                 break
#             try:
#                 position_available = self._add_piece_to_board(pieces[piece_num]) # if there are no more positions for this piece it returns false
#                 #
#                 if not position_available:
#                     pieces.remove(pieces[piece_num])
#             except IndexError:
#                 print("INDEX ERROR")
#                 print("PIECE NUM:", piece_num)
#                 break

#             if self.check_piece_overlapping(pieces[piece_num]):
#                 print("collided") 
#                 pieces[piece_num].reset()
#                 self.recorder.add_step(pieces[piece_num], "Reset Piece position")
#                 piece_num -= 1
#             else:
#                 print("not collided")
#                 piece_num += 1
        
        # position_available = self._add_piece_to_board(pieces[1]) # if there are no more positions for this piece it returns false
            # if not position_available:
            #     pieces.remove(pieces[0])

            # 2 does this piece fit without overlapping any other piece?
                # yes -> 2.1 is there another piece (with a position not tested) to put on game board? 
                #           -> yes: goto 1
                #           -> no: solved
                # no -> go to piece before!
            
        #######
        # position_available = self._add_piece_to_board(pieces[piece_num]) # if there are no more positions for this piece it returns false
        # if not position_available:
        #     pieces.remove(pieces[piece_num])

        # if self.check_piece_overlapping(pieces[piece_num]):
        #     print("collided")
        #     piece_num -= 1
        # else:
        #     print("not collided")
        #     piece_num += 1

        # ######
        # position_available = self._add_piece_to_board(pieces[piece_num]) # if there are no more positions for this piece it returns false
        # if not position_available:
        #     pieces.remove(pieces[piece_num])

        # if self.check_piece_overlapping(pieces[piece_num]):
        #     print("collided")
        #     piece_num -= 1
        # else:
        #     print("not collided")
        #     piece_num += 1
            

        # if self.check_piece_overlapping(pieces[piece_num]):
        #     print("collided")
        #     piece_num -= 1
        # else:
        #     print("not collided")
        #     piece_num += 1

        # 3 put the piece from before to another position
        
        # 4 is there a position that is not set before for this piece?
            # no -> go to 3
            # yes -> goto 2.1     