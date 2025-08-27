import pygame, math, operator, sys, random
# declare global variables
WIDTH, HEIGHT = 700, 400
current_player = "W"
king_position_dict = {"Wking":"e1", "Bking":"e8"}
checking_piece_list = []
en_passant_pawn = ""
move = 0
# initiate pygame and sets up different pygame variables
pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
surface.fill("gray")
pygame.display.set_caption("Opening Chooser!")
#COMICSANS.TTF Font file was uploaded by Lina Von at https://font.download/font/comic-sans 
title_font = pygame.font.Font("COMICSANS.TTF", 45)
mid_font = pygame.font.Font("COMICSANS.TTF", 28)
small_font = pygame.font.Font("COMICSANS.TTF", 20)
clock = pygame.time.Clock()
running = True
font_surface = title_font.render("OPENING CHOOSER", False, "white")
font_rect = font_surface.get_rect(center=(WIDTH/2, 50))

# file taken from github chess-canvas/pgn/chess_openings.csv by Tom Pearson at https://github.com/tomgp/chess-canvas/blob/master/pgn/chess_openings.csv
# find different openings that the user can compare to and explore
with open("chess_openings.csv", "r") as chess_openings_file:
    junk = chess_openings_file.readline()
    code = []
    opening_name = []
    moves = []

    for line in chess_openings_file:
        each_line = line.replace('"', "").strip(",").strip()
        code.append(each_line[0:3])
        each_line = each_line[4:]
        opening_name.append(each_line[:each_line.index("1.")-1])
        moves.append(each_line[each_line.index("1."):])

beginning_font_surface = small_font.render("Beginner", False, "white")
beginning_font_rect = beginning_font_surface.get_rect(center=(130, 340))
advanced_font_surface = small_font.render("Advanced", False, "white")
advanced_font_rect = advanced_font_surface.get_rect(center=(580, 340))
intro_font_surface = small_font.render("Please choose a mode", False, "white")
intro_font_rect = intro_font_surface.get_rect(center=(WIDTH / 2, HEIGHT / 3))

# made by me
find_button_surface = pygame.transform.scale(pygame.image.load("graphics/find.png").convert_alpha(), (130,130))
find_button_surface_rect = find_button_surface.get_rect(midbottom = (550,440))

# reverse button is taken from FlatIcon, designed by Tanah Basah at https://www.flaticon.com/free-icon/undo_7133518?term=reverse&page=1&position=9&origin=search&related_id=7133518
reverse_button_surface = pygame.transform.scale(pygame.image.load("graphics/reverse.png").convert_alpha(), (50,50))
reverse_button_surface_rect = reverse_button_surface.get_rect(bottomright = (700,400))

# reset button is taken from FlatIcon, designed by Freepik at https://www.flaticon.com/free-icon/reset_9908186?term=reset&related_id=9908186
reset_button_surface = pygame.transform.scale(pygame.image.load("graphics/reset.png"), (50,50))
reset_button_surface_rect = reset_button_surface.get_rect(bottomleft = (400,400))

# play_button image is inspired by Stanley Zhao
play_button_surface = pygame.transform.scale(pygame.image.load("graphics/go.png").convert_alpha(), (150, 150))
play_button_rect = play_button_surface.get_rect(center=(WIDTH / 2, 260))
opening_phase = True

# generate_button image is inspired by Stanley Zhao (same image as play_button image)
generate_button = pygame.transform.scale(pygame.image.load("graphics/go.png"), (50,50))
generate_button_rect = generate_button.get_rect(bottomleft = (410,395))

# chessboard_surface image is taken from chess.com at https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.chess.com%2Fterms%2Fchessboard&psig=AOvVaw19HGTYJa_4TWVwH2Uv90Db&ust=1712627462614000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCMCIgc7AsYUDFQAAAAAdAAAAABAE
chessboard_surface = pygame.transform.scale(pygame.image.load("graphics/chessboard.png").convert_alpha(), (400, 400))
chessboard_rect = chessboard_surface.get_rect(midleft=(0, 200))

# beginner_pawn_surface image is taken from Pinterest, designed by Vexels at https://www.pinterest.ca/pin/650418371194789573/
beginner_pawn_surface = pygame.transform.rotozoom((pygame.image.load("graphics/white_pawn.png").convert_alpha()), 20,
                                                  0.4)
beginner_pawn_rect = beginner_pawn_surface.get_rect(center=(100, 200))
beginner = False

# advanced_queen_surface image is taken from Pinterest, designed by Vexels at https://www.pinterest.ca/pin/671740100658786817/
advanced_queen_surface = pygame.transform.rotozoom((pygame.image.load("graphics/advanced_queen.png").convert_alpha()),
                                                   -10, 0.5)
advanced_queen_rect = advanced_queen_surface.get_rect(center=(600, 200))
advanced = False
game_moves_list = []
pieces_group = []
find_phase = False

# reset the chesspieces board 
def reset() -> list:
    return [['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR'],
                     ['BP'] * 8,
                     ["empty"] * 8,
                     ["empty"] * 8,
                     ["empty"] * 8,
                     ["empty"] * 8,
                     ['WP'] * 8,
                     ['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR']
                     ]
chessboard_pieces = reset()

chessboard_notation = [[x + y for x in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']] for y in
                       ['8', '7', '6', '5', '4', '3', '2', '1']]
chessboard_pieces_position = [[[22 + 50 * i, 22 + 50 * y] for i in range(8)] for y in range(8)]


# change the move from the chess_openings.csv file into a list containing different moves
def parse_move_list(random_opening_moves_str:str) -> list:
    i = 0
    random_opening_moves_list = random_opening_moves_str.split(" ")
    for move in random_opening_moves_list:
        if i % 2 == 0:
            random_opening_moves_list[i] = move[move.find(".")+1:]
        i += 1
    return random_opening_moves_list

# using the moves given from the opening file, we can move the pieces on our chessboard accordingly               
def move_pieces(moves:list):
    global current_player
    for move in moves:
        if move[-1] == "+":
            move = move[:-1]
        if "O-O" == move:
            for piece in pieces_group:
                if piece.colour + piece.piece == current_player + "K":
                    piece.castle()
                    piece.move(chessboard_pieces_position[piece.y_list_pos][6])
                    king_rook.move(chessboard_pieces_position[piece.y_list_pos][5]) 
        elif "O-O-O" == move:
            for piece in pieces_group:
                if piece.colour + piece.piece == current_player + "K":
                    piece.castle()
                    piece.move(chessboard_pieces_position[piece.y_list_pos][2])
                    queen_rook.move(chessboard_pieces_position[piece.y_list_pos][3])
        # if it's a pawn - notation is written with a lower character    
        elif not move[0].isupper():
            for piece in pieces_group:
                if current_player == piece.colour and piece.piece == "P" and piece.position[0] == move[0][0] and piece.find_array(move[-2:] if "x" in move else move[0]+move[-1], True) != []:
                    for y in range(len(chessboard_notation)):
                        for x in range(len(chessboard_notation[0])):
                            if chessboard_notation[y][x] == (move[-2:] if "x" in move else move[0]+move[-1]):
                                piece.move(chessboard_pieces_position[y][x])
        # if it's any other pieces - notation is written wih a cap letter
        else:
            for piece in pieces_group:
                piece.change_old_pos()
                # test if the piece matches and it's a legal move available to the piece
                if current_player + move[0] == piece.colour + piece.piece and piece.find_array(move[-2:] if move[-1]!="+" else move[-3:-1], True) != [] and piece.record_move([move[-2:] if move[-1]!="+" else move[-3:-1], "True" if "x" in move else "False"]) == move:
                    for y in range(len(chessboard_notation)):
                        for x in range(len(chessboard_notation[0])):
                            if chessboard_notation[y][x] == move[-2:] if move[-1]!="+" else move[-3:-1]:
                                piece.move(chessboard_pieces_position[y][x])
        current_player = "W" if current_player == "B" else "B"

# find the opening from the chess_openings.csv from the list of moves that the user has played
# recursive function
def find_opening(moves_list:list) -> str:
    pos = 0
    game_moves_str = " ".join(moves_list)
    while len(moves_list) != 0:
        for opening in moves:
            # base case
            if game_moves_str == opening:
                return f"{code[pos]}: {opening_name[pos]} {game_moves_str}"
            pos+=1
        # while the opening is not found with the current moves, remove one move from the move list and continue testing
        return find_opening(moves_list[:-1])

def update(test_surface: pygame.Surface, rect: pygame.Rect) -> None:
    surface.fill("gray")
    surface.blit(test_surface, rect)

# reset all processes such as current player and moved pieces to default
def restart() -> None:
    global chessboard_pieces
    chessboard_pieces = reset()
    pieces_group.empty()
    pieces_group.draw(surface)
    global current_player
    current_player = "W"
    game_moves_list.clear()
    global move
    move = 0
    generate_pieces()

# record the move according to the piece
def record_game_moves(piece) -> None:
    global move
    piece_move = piece.record_move(piece.find_array(chessboard_notation[piece.y_list_pos][piece.x_list_pos], False))
    if current_player == "W":
        move += 1
        game_moves_list.append(f"{move}.{piece_move}")
    else:
        game_moves_list.append(piece_move)
    if not Pieces.is_not_in_check("W" if current_player == "B" else "B"):
        game_moves_list[-1] += "+"

# this algorithm for bliting each text onto the screen is taken from https://stackoverflow.com/a/42015712 made by Ted Klein Bergman
def text_surface_blit(surface:pygame.Surface, pos:tuple, font:pygame.font.Font, max_x:int, text_list: list, colour:tuple):
    x, y = pos
    space = small_font.size(" ")[0]
    for text in text_list:
        text_surface = font.render(text, True, colour)
        text_width, text_height = text_surface.get_size()
        if x + text_width >= max_x:
            x = pos[0]
            y += text_height
        surface.blit(text_surface, (x,y))
        x += text_width + space
    return y + font.size(" ")[1]

# generate a list from the opening file with the code (e.g A00), the opening name, and the moves
def random_opening() -> tuple:
    x = random.randint(0,len(moves)-1)
    return (code[x], opening_name[x], moves[x])

# declare a parent class of pieces of which all pieces on the chessboard will inherit from
class Pieces(pygame.sprite.Sprite):

    def __init__(self, image: str, colour: str, position: str, x: int, y: int, y_list_pos: int, x_list_pos: int,
                 piece: str) -> None:
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (40, 40))
        self.colour = colour
        self.position = position
        self.x = x  # each square is 50 x 50
        self.y = y
        self.rect = self.image.get_rect(center=(x, y))
        self.x_list_pos = x_list_pos
        self.y_list_pos = y_list_pos
        self.piece = piece
        self.old_pos_x = chessboard_notation[self.y_list_pos][self.x_list_pos][1]
        self.old_pos_y = chessboard_notation[self.y_list_pos][self.x_list_pos][0]
        self.moves_list = []
    
    # move to a given position given by a tuple of position, returns true if moved successfully 
    def move(self, new_pos: tuple) -> bool:
        closest_square_x, closest_square_y = self.get_new_square(new_pos)
        selected_piece = chessboard_pieces[self.y_list_pos][self.x_list_pos]
        chessboard_pieces[self.y_list_pos][self.x_list_pos] = "empty"
        self.change_old_pos()
        self.x_list_pos = closest_square_x
        self.y_list_pos = closest_square_y
        chessboard_pieces[closest_square_y][closest_square_x] = selected_piece
        self.position = chessboard_notation[self.y_list_pos][self.x_list_pos]
        self.x = chessboard_pieces_position[self.y_list_pos][self.x_list_pos][0]
        self.y = chessboard_pieces_position[self.y_list_pos][self.x_list_pos][1]
        self.rect = self.image.get_rect(center=(chessboard_pieces_position[self.y_list_pos][self.x_list_pos]))
        surface.fill('gray')
        surface.blit(chessboard_surface, chessboard_rect)
        pieces_group.update()
        # if the pawn moves two square, the pawn should be stored in a global variable that allows it to be captured with enpassant
        global en_passant_pawn
        if en_passant_pawn != "":
            en_passant_pawn = ""
        if self.piece == "P" and self.en_passant_check(chessboard_notation[self.y_list_pos][self.x_list_pos]):
            en_passant_pawn = self
        return True
            
    def change_old_pos(self):
        self.old_pos_x = chessboard_notation[self.y_list_pos][self.x_list_pos][1]
        self.old_pos_y = chessboard_notation[self.y_list_pos][self.x_list_pos][0]

    def update(self):
        if chessboard_pieces[self.y_list_pos][self.x_list_pos] == "empty" or not chessboard_pieces[self.y_list_pos][self.x_list_pos] == self.colour + self.piece:
            self.kill()
            pieces_group.draw(surface)

    # check if the move that the is user is trying to make is a legal move. Returns true if so else return false. 
    def is_legal_move(self, move: str) -> bool:
        if not self.will_not_cause_check(move):
            return False
        # check if the move is in the piece's legal moves list. 
        if self.can_move_to() != []:
            for array in self.moves_list:
                if move in array:
                    if "kingcastle" in array:
                        king_rook.move(chessboard_pieces_position[self.y_list_pos][5])
                    if "queencastle" in array:
                        queen_rook.move(chessboard_pieces_position[self.y_list_pos][3])
                    if checking_piece_list != []:
                        checking_piece_list.clear()
                    if "enpassantcapture" in array:
                        en_passant_pawn.kill()
                        chessboard_pieces[en_passant_pawn.y_list_pos][en_passant_pawn.x_list_pos] = "empty"
                        pieces_group.draw(surface)
                    return True
        return False
        
    def can_move_to(self) -> list:
        return []

    @staticmethod
    # check if the user is not in check. Returns true if the user is not, returns false otherwise
    def is_not_in_check(player:str) -> bool:
        checking_piece_list.clear()
        for piece in pieces_group:
            if piece.colour == player:
                continue
            if chessboard_pieces[piece.y_list_pos][piece.x_list_pos] == "empty" or chessboard_pieces[piece.y_list_pos][piece.x_list_pos] != piece.colour + piece.piece:
                continue
            # for every move of pieces opposite colour of the current player, check if the position of the king is one of the pieces' legal moves. 
            for move in piece.can_move_to():
                if king_position_dict[f"{player}king"] in move:
                    checking_piece_list.append(piece)
        if checking_piece_list != []:
            return False
        return True

    # check if the player who's moving will cause a check with the current move. Return true if it will not else return false
    def will_not_cause_check(self, move:str) -> bool:
        selected_piece = chessboard_pieces[self.y_list_pos][self.x_list_pos]
        chessboard_pieces[self.y_list_pos][self.x_list_pos] = "empty"
        for y in range(len(chessboard_notation)):
            for x in range(len(chessboard_notation[0])):
                if chessboard_notation[y][x] == move:
                    temp, temp_y, temp_x = chessboard_pieces[y][x], y, x
                    chessboard_pieces[y][x] = selected_piece
        if selected_piece[1] == "K":
            old_pos_y = king_position_dict[f"{current_player}king"]
            king_position_dict[f"{current_player}king"] = move
        executed = self.is_not_in_check(current_player)
        chessboard_pieces[self.y_list_pos][self.x_list_pos] = selected_piece
        chessboard_pieces[temp_y][temp_x] = temp
        if selected_piece[1] == "K":
            king_position_dict[f"{current_player}king"] = old_pos_y
        return executed

    @staticmethod
    def get_new_square(new_pos: tuple) -> tuple:
        min_distance = math.sqrt(math.pow(new_pos[0] - chessboard_pieces_position[0][0][0], 2) + math.pow(
            new_pos[1] - chessboard_pieces_position[0][0][1], 2))
        closest_square_x = 0
        closest_square_y = 0
        for x in range(len(chessboard_pieces)):
            for y in range(len(chessboard_pieces)):
                test_distance = math.sqrt(math.pow(new_pos[0] - chessboard_pieces_position[x][y][0], 2) + math.pow(
                    new_pos[1] - chessboard_pieces_position[x][y][1], 2))
                if test_distance < min_distance:
                    min_distance = test_distance
                    closest_square_x = y
                    closest_square_y = x
        return closest_square_x, closest_square_y

    # make sure that the square user clicked on is not the square it is already on
    def is_same_square(self, closest_square_y: int, closest_square_x: int) -> bool:
        if self.y_list_pos == closest_square_y and self.x_list_pos == closest_square_x:
            return True
        return False
    
    # record the move according to the pieces and captures.
    def record_move(self, move:list) -> str:
        i = 1
        move_recorded = self.piece + move[0]
        for piece in pieces_group:
            if piece.colour + piece.piece == self.colour + self.piece and piece != self and move in (piece.can_move_to() if not piece.moves_list else piece.moves_list):
                if piece.position[0] == self.old_pos_y:
                    move_recorded = f"{move_recorded[0]}{self.old_pos_x}{move_recorded[1:]}"
                else:
                    move_recorded = f"{move_recorded[0]}{self.old_pos_y}{move_recorded[1:]}"
                i = 2
        if "True" in move:
            move_recorded = f"{move_recorded[0:i]}x{move_recorded[i:]}"
        return move_recorded
    
    # check all the squares a piece can move to diagonally (bishop/queen)
    def diagonal_moves_check(self) -> list:
        signs = ["+", "+", "+", "-", "-", "+", "-", "-"]
        for x_sign, y_sign in zip(signs[0::2], signs[1::2]):
            self.help_can_diagonal_move(x_sign, y_sign)
        return self.moves_list

    def help_can_diagonal_move(self, x_sign:str, y_sign:str) -> None:
        ops = {"+":operator.add, "-":operator.sub}
        for i in range(1,7):
            if not (0<=ops[y_sign](self.y_list_pos,i)<len(chessboard_notation) and 0<=ops[x_sign](self.x_list_pos,i)<len(chessboard_notation[0])):
                break
            if chessboard_pieces[ops[y_sign](self.y_list_pos,i)][ops[x_sign](self.x_list_pos,i)][0] == self.colour:
                break
            if not chessboard_pieces[ops[y_sign](self.y_list_pos,i)][ops[x_sign](self.x_list_pos,i)] == "empty" and not chessboard_pieces[ops[y_sign](self.y_list_pos,i)][ops[x_sign](self.x_list_pos,i)][1] == "K" :
                self.moves_list.append([chessboard_notation[ops[y_sign](self.y_list_pos,i)][ops[x_sign](self.x_list_pos,i)], "True"])
                break
            self.moves_list.append([chessboard_notation[ops[y_sign](self.y_list_pos,i)][ops[x_sign](self.x_list_pos,i)], "False"])

    # check all the squares a piece can move to vertically or horizontally (rook/queen)
    def straight_moves_check(self) -> list:
        for sign in ["+", "-"]:
            self.help_can_straight_move(sign)
        return self.moves_list

    def help_can_straight_move(self, sign:str) -> None:
        ops = {"+":operator.add, "-":operator.sub}
        i = 1 
        while 0<=ops[sign](self.y_list_pos,i)<len(chessboard_pieces) and not chessboard_pieces[ops[sign](self.y_list_pos,i)][self.x_list_pos][0] == self.colour:
            if not chessboard_pieces[ops[sign](self.y_list_pos,i)][self.x_list_pos] == "empty" and not chessboard_pieces[ops[sign](self.y_list_pos,i)][self.x_list_pos][1] == "K" :
                self.moves_list.append([chessboard_notation[ops[sign](self.y_list_pos,i)][self.x_list_pos], "True"])
                break
            self.moves_list.append([chessboard_notation[ops[sign](self.y_list_pos,i)][self.x_list_pos], "False"])
            i += 1
        z = 1
        while 0<=ops[sign](self.x_list_pos,z)<len(chessboard_pieces[0]) and not chessboard_pieces[self.y_list_pos][ops[sign](self.x_list_pos,z)][0] == self.colour:
            if not chessboard_pieces[self.y_list_pos][ops[sign](self.x_list_pos,z)] == "empty" and not chessboard_pieces[self.y_list_pos][ops[sign](self.x_list_pos,z)][1] == "K":
                self.moves_list.append([chessboard_notation[self.y_list_pos][ops[sign](self.x_list_pos,z)], "True"])
                break
            self.moves_list.append([chessboard_notation[self.y_list_pos][ops[sign](self.x_list_pos,z)], "False"])
            z += 1 
    
    # returns an array from the piece's legal move list from the move. Returns the array if found else return an empty list
    def find_array(self, move:str, update:bool) -> list:
        for array in self.can_move_to() if update else self.moves_list:
            if move in array:
                return array
        return []

# subclass of Pieces, only for pawns.
class Pawn(Pieces):

    def __init__(self, image, colour, position, x, y, y_list_pos, x_list_pos, piece):
        super().__init__(image, colour, position, x, y, y_list_pos, x_list_pos, piece)
        self.first_move = True

    def can_move_to(self) -> list:
        self.moves_list.clear()
        adjust = -1 if self.colour == "W" else 1
        if self.first_move and chessboard_pieces[self.y_list_pos + 2*adjust][self.x_list_pos] == "empty":
            self.moves_list.append([chessboard_notation[self.y_list_pos + 2 * adjust][self.x_list_pos], "False", "enpassant"])
        if 0<self.y_list_pos+adjust < len(chessboard_pieces) and chessboard_pieces[self.y_list_pos+adjust][self.x_list_pos] == "empty":
            self.moves_list.append([chessboard_notation[self.y_list_pos + adjust][self.x_list_pos], "False"])
        ops = {"+":operator.add, "-":operator.sub}
        signs = ["+", '-']
        for sign in signs:
            if 0 <= ops[sign](self.x_list_pos,adjust) < len(chessboard_pieces[0]) and 0 <= ops[sign](self.y_list_pos,adjust)< len(chessboard_pieces):
                if not chessboard_pieces[self.y_list_pos+adjust][ops[sign](self.x_list_pos,adjust)] == "empty" and not chessboard_pieces[self.y_list_pos+adjust][ops[sign](self.x_list_pos,adjust)][0] == self.colour:
                    self.moves_list.append([chessboard_notation[self.y_list_pos+adjust][ops[sign](self.x_list_pos,adjust)], "True"])
        self.en_passant_move()
        return self.moves_list
        
    def move(self, new_pos: tuple) -> bool:
        executed = Pieces.move(self, new_pos)
        if executed:
            self.first_move = False
        return executed

    # enpassant handling
    def en_passant_move(self) -> None:
        for piece in pieces_group:
            if piece.colour != self.colour and piece.piece == "P" and piece == en_passant_pawn and piece.y_list_pos == self.y_list_pos:
                if self.x_list_pos + 1 < len(chessboard_pieces) and piece.x_list_pos == self.x_list_pos + 1:
                    self.moves_list.append([chessboard_notation[self.y_list_pos-1 if current_player == "W" else self.y_list_pos+1][self.x_list_pos+1],"True","enpassantcapture"])
                if 0 <= self.x_list_pos - 1 and piece.x_list_pos == self.x_list_pos - 1:
                    self.moves_list.append([chessboard_notation[self.y_list_pos-1 if current_player == "W" else self.y_list_pos+1][self.x_list_pos-1],"True","enpassantcapture"])
    
    def en_passant_check(self, move:str) -> bool:
        move_list = self.find_array(move, False)
        if move_list != [] and "enpassant" in move_list:
            return True
        return False

    def record_move(self, move: list) -> str:
        move_recorded = chessboard_notation[self.y_list_pos][self.x_list_pos]
        if "True" in move:
            move_recorded = self.old_pos_y + "x" + move_recorded
        return move_recorded

#subclass of Pieces for Knights
class Knight(Pieces):

    def __init__(self, image, colour, position, x, y, y_list_pos, x_list_pos, piece):
        super().__init__(image, colour, position, x, y, y_list_pos, x_list_pos, piece)

    def can_move_to(self) -> list:
        self.moves_list = []
        vertical = [1,-1,2,-2]
        for ver in vertical:
            horizontal = [2,-2] if abs(ver) == 1 else [1,-1]
            for hor in horizontal:
                if 0 <= self.y_list_pos+ver < len(chessboard_pieces) and 0<= self.x_list_pos+hor< len(chessboard_pieces[0]) and self.colour != chessboard_pieces[self.y_list_pos+ver][self.x_list_pos+hor][0]:
                    if chessboard_pieces[self.y_list_pos+ver][self.x_list_pos+hor] != "empty" and chessboard_pieces[self.y_list_pos+ver][self.x_list_pos+hor][1] != "K" :
                        self.moves_list.append([chessboard_notation[self.y_list_pos+ver][self.x_list_pos+hor], "True"])
                    else:
                        self.moves_list.append([chessboard_notation[self.y_list_pos+ver][self.x_list_pos+hor], "False"]) 
        return self.moves_list
     
#subclass of Pieces for Bishops                  
class Bishop(Pieces):

    def __init__(self, image, colour, position, x, y, y_list_pos, x_list_pos, piece):
        super().__init__(image, colour, position, x, y, y_list_pos, x_list_pos, piece)

    def can_move_to(self) -> list:
        self.moves_list = []
        return super().diagonal_moves_check()

# subclass of Pieces for Queens
class Queen(Pieces):

    def __init__(self, image, colour, position, x, y, y_list_pos, x_list_pos, piece):
        super().__init__(image, colour, position, x, y, y_list_pos, x_list_pos, piece)

    def can_move_to(self) -> list:
        self.moves_list = []
        return super().diagonal_moves_check() + super().straight_moves_check()

# subclass of Pieces for Rooks
class Rook(Pieces):

    def __init__(self, image, colour, position, x, y, y_list_pos, x_list_pos, piece):
        super().__init__(image, colour, position, x, y, y_list_pos, x_list_pos, piece)
        self.moved = False

    def can_move_to(self) -> list:
        self.move_list = []
        return super().straight_moves_check()
    
    def move(self, new_pos: tuple) -> bool:
        executed = Pieces.move(self, new_pos)
        if executed:
            self.moved = True
        return executed

# subclass of Pieces for Kings
class King(Pieces):

    def __init__(self, image, colour, position, x, y, y_list_pos, x_list_pos, piece):
        super().__init__(image, colour, position, x, y, y_list_pos, x_list_pos, piece)
        self.moved = False
 
    def castle(self) -> None:
        global king_rook, queen_rook
        king_rook, queen_rook = "", ""
        for piece in pieces_group:
            if piece.x_list_pos == 7 and piece.y_list_pos == self.y_list_pos and piece.colour+piece.piece == self.colour+"R" and king_rook != None:
                if piece.moved == False:
                    king_rook = piece
            elif piece.x_list_pos == 0 and piece.y_list_pos == self.y_list_pos and piece.colour+piece.piece == self.colour+"R" and queen_rook != None:
                if piece.moved == False:
                    queen_rook = piece
            if piece.colour != current_player and piece.piece != "K":
                for array in piece.moves_list:
                    if chessboard_notation[self.y_list_pos][5] in array:
                        king_rook = None
                    elif chessboard_notation[self.y_list_pos][4] in array or chessboard_notation[self.y_list_pos][3] in array:
                        queen_rook = None
        if self.moved == False and Pieces.is_not_in_check(current_player): 
            if chessboard_pieces[self.y_list_pos][5] == "empty" and chessboard_pieces[self.y_list_pos][6] == "empty" and king_rook != None and king_rook != "":
                self.moves_list.append([f"g{8-self.y_list_pos}", "False", "kingcastle"])
                if [f"f{8-self.y_list_pos}", "False"] in piece.moves_list:
                    piece.moves_list.remove([f"f{8-self.y_list_pos}", "False"])
                piece.moves_list.append([f"f{8-self.y_list_pos}", "False"])
            if chessboard_pieces[self.y_list_pos][2] == "empty" and chessboard_pieces[self.y_list_pos][3] == "empty" and queen_rook != None and queen_rook != "":
                self.moves_list.append([f"c{8-self.y_list_pos}", "False", "queencastle"])
                if [f"d{8-self.y_list_pos}", "False"] in piece.moves_list:
                    piece.moves_list.remove([f"d{8-self.y_list_pos}", "False"])
                piece.moves_list.append([f"d{8-self.y_list_pos}", "False"]) 

    def can_move_to(self) -> list:
        self.moves_list.clear()
        adjust_list = [0,1,-1]
        for y in adjust_list:
            for x in adjust_list:
                if 0<=self.y_list_pos+y < len(chessboard_pieces) and 0<=self.x_list_pos+x < len(chessboard_pieces[0]):
                    if chessboard_pieces[self.y_list_pos+y][self.x_list_pos+x][0] == "e":
                        self.moves_list.append([chessboard_notation[self.y_list_pos+y][self.x_list_pos+x], "False"])
                    elif chessboard_pieces[self.y_list_pos+y][self.x_list_pos+x][0] != self.colour:
                        self.moves_list.append([chessboard_notation[self.y_list_pos+y][self.x_list_pos+x], "True"])
        if current_player == self.colour:
            self.castle()
        return self.moves_list

    def move(self, new_pos: tuple) -> bool:
        executed = Pieces.move(self, new_pos)
        if executed:
            self.moved = True
            king_position_dict[f"{self.colour}king"] = self.position
        return executed
    
    def record_move(self, move: list) -> str:
        if "kingcastle" in move:
            return "O-O"
        elif "queencastle" in move:
            return "O-O-O"
        return super().record_move(move)

# generate objects of the Pieces class according to the chessboard_pieces list.
def generate_pieces():
    for x in range(len(chessboard_pieces[0])):
        for y in range(len(chessboard_pieces)):
            current_piece = chessboard_pieces[x][y]
            if not current_piece == "empty":
                colour = current_piece[0]
                piece = current_piece[1]
                match piece:
                    case "P":
                        # W_playing_pawn image is taken from flaticon, designed by Good Ware at https://www.flaticon.com/free-icon/pawn_864639?term=pawn&page=1&position=4&origin=search&related_id=864639
                        # B_playing_pawn image is taken from flaticon, designed by Andrejs Kirma at https://www.flaticon.com/free-icon/pawn_6378368?term=pawn&page=1&position=3&origin=search&related_id=6378368
                        pawn = Pawn(f"graphics/{colour}_playing_pawn.png", colour, chessboard_notation[x][y],
                                    chessboard_pieces_position[x][y][0], chessboard_pieces_position[x][y][1], x, y, "P")
                        pieces_group.add(pawn)
                    case "R":
                        # W_playing_rook image is taken from flaticon, designed by Good Ware at https://www.flaticon.com/free-icon/rook_864641?term=rook&page=1&position=10&origin=search&related_id=864641
                        # B_playing_rook image is taken from flaticon, designed by deemakdaksina at https://www.flaticon.com/free-icon/rook_1626883?term=rook&page=1&position=1&origin=search&related_id=1626883
                        rook = Rook(f"graphics/{colour}_playing_rook.png", colour, chessboard_notation[x][y],
                                    chessboard_pieces_position[x][y][0], chessboard_pieces_position[x][y][1], x, y, "R")
                        pieces_group.add(rook)
                    case "N":
                        # W_playing_knight image is taken from flaticon, designed by Good Ware at https://www.flaticon.com/free-icon/horse_864637?term=knight&page=1&position=23&origin=search&related_id=864637
                        # B_playing_pawn image is taken from flaticon, designed by SBTS2018 at https://www.flaticon.com/free-icon/chess_11497377?term=knight&page=1&position=8&origin=search&related_id=11497377
                        knight = Knight(f"graphics/{colour}_playing_knight.png", colour, chessboard_notation[x][y],
                                        chessboard_pieces_position[x][y][0], chessboard_pieces_position[x][y][1], x, y, "N")
                        pieces_group.add(knight)
                    case "B":
                        # W_playing_bishop image is taken from flaticon, designed by Good Ware at https://www.flaticon.com/free-icon/bishop_864631?term=bishop&page=1&position=28&origin=search&related_id=864631
                        # B_playing_bishop image is taken from flaticon, designed by DinosoftLabs at https://www.flaticon.com/free-icon/bishop_4744929?term=bishop&page=1&position=6&origin=search&related_id=4744929
                        bishop = Bishop(f"graphics/{colour}_playing_bishop.png", colour, chessboard_notation[x][y],
                                        chessboard_pieces_position[x][y][0], chessboard_pieces_position[x][y][1], x, y, "B")
                        pieces_group.add(bishop)
                    case "Q":
                        # W_playing_queen image is taken from flaticon, designed by Good Ware at https://www.flaticon.com/free-icon/queen_864640?term=chess+queen&page=1&position=10&origin=search&related_id=864640
                        # B_playing_queen image is taken from flaticon, designed by Freepik at https://www.flaticon.com/free-icon/queen-chess-piece-black-shape_44502?term=queen&page=1&position=29&origin=search&related_id=44502
                        queen = Queen(f"graphics/{colour}_playing_queen.png", colour, chessboard_notation[x][y],
                                    chessboard_pieces_position[x][y][0], chessboard_pieces_position[x][y][1], x, y, "Q")
                        pieces_group.add(queen)
                    case "K":
                        # W_playing_king image is taken from flaticon, designed by Good Ware at https://www.flaticon.com/free-icon/king_864638?term=chess+king&page=1&position=34&origin=search&related_id=864638
                        # B_playing_king image is taken from flaticon, designed by Freepik at https://www.flaticon.com/free-icon/king_3522646?term=king&page=1&position=20&origin=search&related_id=3522646
                        king = King(f"graphics/{colour}_playing_king.png", colour, chessboard_notation[x][y],
                                    chessboard_pieces_position[x][y][0], chessboard_pieces_position[x][y][1], x, y, "K")
                        pieces_group.add(king)
                    case _:
                        raise Exception("Piece Not Found!")
is_selected = False
selected = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if opening_phase:
                intro_font_surface = small_font.render("Please choose a mode", False, "white")
                # when mouse is clicked on one of the three buttons on the home page
                if play_button_rect.collidepoint(pygame.mouse.get_pos()):
                    if beginner or advanced:
                        opening_phase = False
                        surface.fill('gray')
                        pieces_group = pygame.sprite.Group()
                        restart()
                elif beginner_pawn_rect.collidepoint(pygame.mouse.get_pos()):
                    if advanced:
                        advanced = False
                    beginner = True
                    beginner_pawn_surface.set_alpha(5)
                    advanced_queen_surface.set_alpha(255)
                    update(beginner_pawn_surface, beginner_pawn_rect)
                    intro_font_surface = small_font.render("Beginner mode selected!", False, "white")
                    update(intro_font_surface, intro_font_rect)
                elif advanced_queen_rect.collidepoint(pygame.mouse.get_pos()):
                    if beginner:
                        beginner = False
                    advanced = True
                    advanced_queen_surface.set_alpha(5)
                    beginner_pawn_surface.set_alpha(255)
                    update(advanced_queen_surface, advanced_queen_rect)
                    intro_font_surface = small_font.render("Advance mode selected!", False, "white")
                    update(intro_font_surface, intro_font_rect)
            if not opening_phase and advanced:
                # when reset button is clicked, the chessboard pieces return to their starting position
                if reset_button_surface_rect.collidepoint(pygame.mouse.get_pos()):
                    restart()
                if is_selected and selected is not None:
                    pos = pygame.mouse.get_pos()
                    x, y = selected.get_new_square(pos)
                    if (not selected.is_same_square(y,x) and selected.is_legal_move(chessboard_notation[y][x]) and
                    selected.move(pygame.mouse.get_pos())):
                        record_game_moves(selected)
                        if current_player == "W":
                            current_player = "B"
                        else:
                            current_player = "W"
                    selected = None
                    is_selected = False
                else:
                    for sprite in pieces_group:
                        pos = pygame.mouse.get_pos()
                        if sprite.rect.collidepoint(pos) and not is_selected:
                            selected = sprite
                            # make sure the player is selecting their piece on their own turn
                            if (current_player == "W" and selected.colour == "W") or (current_player == "B" and selected.colour == "B"):
                                is_selected = True
                # goes into find_phase 
                if find_button_surface_rect.collidepoint(pygame.mouse.get_pos()):
                    advanced = False
                    find_phase = True
            # goes back to the previous page 
            if reverse_button_surface_rect.collidepoint(pygame.mouse.get_pos()):
                surface.fill("gray")
                if advanced:
                    opening_phase = True
                    advanced = False
                elif find_phase:
                    advanced = True
                    find_phase = False
                elif beginner:
                    beginner = False
                    opening_phase = True
            # when the generated button is clicked on beginner page, moves the chess pieces on the board so that it corresponds to the opening 
            if generate_button_rect.collidepoint(pygame.mouse.get_pos()) and beginner:
                restart()
                random_opening_list = random_opening()
                random_opening_moves_list = parse_move_list(random_opening_list[2])
                move_pieces(random_opening_moves_list)
                # shows the player the random opening's code, name and moves
                text_surface_blit(surface, (410,30),mid_font, WIDTH, random_opening_list[0].split(" "), "black")
                y = text_surface_blit(surface, (410,80),mid_font, WIDTH, random_opening_list[1].split(" "), "black")
                text_surface_blit(surface, (410,y+10),small_font, WIDTH, random_opening_list[2].split(" "), "black")
    if opening_phase:
        surface.blits([(font_surface, font_rect), (play_button_surface, play_button_rect),
                       (beginner_pawn_surface, beginner_pawn_rect), (advanced_queen_surface, advanced_queen_rect),
                       (beginning_font_surface, beginning_font_rect), (advanced_font_surface, advanced_font_rect),
                       (intro_font_surface, intro_font_rect)])
    else:
        # graphics when in diffent phases of the program
        if advanced:
            # W_playing_pawn image is taken from flaticon, designed by Good Ware at https://www.flaticon.com/free-icon/pawn_864639?term=pawn&page=1&position=4&origin=search&related_id=864639
            white_turn_surface = pygame.transform.scale(pygame.image.load("graphics/W_playing_pawn.png").convert_alpha(), (60,60))
            white_turn_surface_rect = white_turn_surface.get_rect(topleft = (405, 0))
            surface.blit(white_turn_surface,white_turn_surface_rect)
            # B_playing_pawn image is taken from flaticon, designed by Andrejs Kirma at https://www.flaticon.com/free-icon/pawn_6378368?term=pawn&page=1&position=3&origin=search&related_id=6378368
            black_turn_surface = pygame.transform.scale(pygame.image.load("graphics/B_playing_pawn.png").convert_alpha(), (60,60))
            black_turn_surface_rect = black_turn_surface.get_rect(topleft = (470, 0))
            surface.blit(black_turn_surface, black_turn_surface_rect)
            surface.fill("gray")
            surface.blit(reset_button_surface,reset_button_surface_rect)
            if current_player == "W":
                white_turn_surface.set_alpha(255)
                black_turn_surface.set_alpha(30)
                surface.blit(white_turn_surface,white_turn_surface_rect)
                surface.blit(black_turn_surface, black_turn_surface_rect)
            else:
                black_turn_surface.set_alpha(255)
                white_turn_surface.set_alpha(30)
                surface.blit(white_turn_surface,white_turn_surface_rect)
                surface.blit(black_turn_surface, black_turn_surface_rect)
            
            current_surface = small_font.render("Currently ", False, "black")
            current_surface_rect = current_surface.get_rect(topleft = (550, 0))
            surface.blit(current_surface, current_surface_rect)

            selected_surface = small_font.render("Selected: ", False, "black")
            selected_surface_rect = selected_surface.get_rect(topleft = (550, current_surface.get_size()[1]))
            surface.blit(selected_surface, selected_surface_rect)
            if selected != None:
                piece_surface = pygame.transform.scale(selected.image, (60,60))
                piece_surface_rect = piece_surface.get_rect(topleft = (550+current_surface.get_size()[0], 0))
                surface.blit(piece_surface, piece_surface_rect)
            surface.blit(find_button_surface, find_button_surface_rect)
            text_surface_blit(surface, (410,90), small_font, WIDTH, game_moves_list, (0,0,0))
        if beginner:
            surface.blit(generate_button, generate_button_rect)
        if not find_phase:
            surface.blit(chessboard_surface, chessboard_rect)
            pieces_group.draw(surface)
        else:
            surface.fill("gray")
            surface.blit(title_font.render("Your moves:", True, (1,50,32)), (5,0))
            surface.blit(title_font.render("Opening:", True, "black"), (WIDTH/2,0))
            text_surface_blit(surface, (5, 70), mid_font, WIDTH/2, game_moves_list, (1,50,32))
            opening = find_opening(game_moves_list)
            text_surface_blit(surface, (WIDTH/2,70), mid_font, WIDTH, (opening if opening != None else "Opening not found").split(" "), (0,0,0))
        surface.blit(reverse_button_surface, reverse_button_surface_rect)

    pygame.display.update()
    clock.tick(60)