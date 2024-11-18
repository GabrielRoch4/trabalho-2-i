# for representing the board as a matrix and doing operations on it
import numpy as np
# for gui
import pygame
# for exiting the gui
import sys
# for calculations, for example with infinity
import math
# for delaying execution of certain events
from threading import Timer
# for generating random values, for example for 1st turn
import random

import time

# global constant variables
# -------------------------------

# row and column count
ROWS = 7
COLS = 8

# turns
PLAYER_TURN = 0
AI_TURN = 1

# pieces represented as numbers
PLAYER_PIECE = 1
AI_PIECE = 2

# colors for GUI
BLUE = (0, 0, 153)  # MENU_BLUE
RED = (255, 99, 71)  # MENU_RED
YELLOW = (239, 174, 84)  # MENU_YELLOW
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def show_menu_screen(screen):
    # Colors
    MENU_BLUE = (0, 0, 153)
    MENU_YELLOW = (239, 174, 84)
    MENU_GREEN = (0, 128, 0)
    MENU_RED = (255, 99, 71)
    WHITE = (255, 255, 255)
    HOVER_COLOR = (255, 215, 0)  # Hover effect color (light yellow)

    # Font (Using downloaded font)
    font_title = pygame.font.Font("Galindo-Regular.ttf", 60)  # Tamanho reduzido
    font_label = pygame.font.Font("Galindo-Regular.ttf", 25)
    font_option = pygame.font.Font("Galindo-Regular.ttf", 23)
    font_button = pygame.font.Font("Galindo-Regular.ttf", 30)

    # Variables
    clock = pygame.time.Clock()
    ball_offset = 0
    ball_direction = 1
    input_active = False
    input_text = ""
    selected_algorithm = "Mini-max"
    selected_ply = "1"

    # Options for selection
    algorithm_options = ["Mini-max", "Alfa-beta"]
    ply_options = ["1", "2", "3", "4"]
    algorithm_rects = []
    ply_rects = []

    # Animation settings
    ball_speed = 2

    def draw_title():
        """Draw the title with animated balls."""
        title_surface = font_title.render("Connect4 da Dani", True, MENU_YELLOW)
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(title_surface, title_rect)

        # Ball animation
        nonlocal ball_offset, ball_direction
        if ball_offset >= 10 or ball_offset <= -10:
            ball_direction *= -1
        ball_offset += ball_speed * ball_direction

    def draw_input_field(mouse_pos):
        """Draw the input field for the player's name with hover effect."""
        label = font_label.render("Insira seu nome:", True, MENU_YELLOW)
        screen.blit(label, (screen.get_width() // 2 - 130, 120))

        input_rect = pygame.Rect((screen.get_width() // 2 - 150, 160), (300, 40))
        input_hover = input_rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, HOVER_COLOR if input_hover else MENU_YELLOW, input_rect, 2)

        input_surface = font_option.render(input_text or "Seu nome", True, WHITE)
        screen.blit(input_surface, (input_rect.x + 10, input_rect.y + 5))
        return input_rect

    def draw_algorithm_options(mouse_pos):
        """Draw algorithm options with hover effect."""
        label = font_label.render("Escolha o algoritmo:", True, MENU_YELLOW)
        screen.blit(label, (screen.get_width() // 2 - 150, 220))

        x, y = screen.get_width() // 2 - 150, 260
        for option in algorithm_options:
            rect = pygame.Rect((x, y), (140, 40))
            color = MENU_YELLOW if option == selected_algorithm else WHITE
            if rect.collidepoint(mouse_pos):
                color = HOVER_COLOR
            pygame.draw.rect(screen, color, rect, border_radius=5)
            text_surface = font_option.render(option, True, MENU_BLUE)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)
            algorithm_rects.append((rect, option))
            x += 160

    def draw_ply_options(mouse_pos):
        """Draw depth options with hover effect."""
        label = font_label.render("Escolha a profundidade (ply):", True, MENU_YELLOW)
        screen.blit(label, (screen.get_width() // 2 - 150, 320))

        x, y = screen.get_width() // 2 - 150, 360
        for option in ply_options:
            rect = pygame.Rect((x, y), (60, 40))
            color = MENU_YELLOW if option == selected_ply else WHITE
            if rect.collidepoint(mouse_pos):
                color = HOVER_COLOR
            pygame.draw.rect(screen, color, rect, border_radius=5)
            text_surface = font_option.render(option, True, MENU_BLUE)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)
            ply_rects.append((rect, option))
            x += 80

    def draw_play_button(mouse_pos):
        """Draw the play button with hover effect."""
        play_rect = pygame.Rect((screen.get_width() // 2 - 100, 440), (200, 50))
        color = MENU_YELLOW if not play_rect.collidepoint(mouse_pos) else HOVER_COLOR
        pygame.draw.rect(screen, color, play_rect, border_radius=5)
        play_text = font_button.render("Jogar", True, MENU_BLUE)
        play_text_rect = play_text.get_rect(center=play_rect.center)
        screen.blit(play_text, play_text_rect)
        return play_rect

    # Main loop
    running = True
    while running:
        screen.fill(MENU_BLUE)
        algorithm_rects.clear()
        ply_rects.clear()

        mouse_pos = pygame.mouse.get_pos()
        draw_title()
        input_rect = draw_input_field(mouse_pos)
        draw_algorithm_options(mouse_pos)
        draw_ply_options(mouse_pos)
        play_button = draw_play_button(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False

                for rect, option in algorithm_rects:
                    if rect.collidepoint(event.pos):
                        selected_algorithm = option

                for rect, option in ply_rects:
                    if rect.collidepoint(event.pos):
                        selected_ply = option

                if play_button.collidepoint(event.pos):
                    return input_text, selected_algorithm, selected_ply

            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        pygame.display.flip()
        clock.tick(60)


# Continuando com o restante do jogo (código de lógica e loop principal segue o mesmo a partir daqui).



# global constant variables
# -------------------------------

# row and column count
ROWS = 7
COLS = 8

# turns
PLAYER_TURN = 0
AI_TURN = 1

# pieces represented as numbers
PLAYER_PIECE = 1
AI_PIECE = 2

# colors for GUI
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# various functions used by the game
# -------------------------------

# using numpy, create an empty matrix of 6 rows and 7 columns
def create_board():
    board = np.zeros((ROWS, COLS))
    return board


# add a piece to a given location, i.e., set a position in the matrix as 1 or 2
def drop_piece(board, row, col, piece):
    board[row][col] = piece


# checking that the top row of the selected column is still not filled
# i.e., that there is still space in the current column
# note that indexing starts at 0
def is_valid_location(board, col):
    return board[0][col] == 0


# checking where the piece will fall in the current column
# i.e., finding the first zero row in the given column
def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r


# calculating if the current state of the board for player or AI is a win
def winning_move(board, piece):
    # checking horizontal 'windows' of 4 for win
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # checking vertical 'windows' of 4 for win
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # checking positively sloped diagonals for win
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    # checking negatively sloped diagonals for win
    for c in range(3,COLS):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c-1] == piece and board[r-2][c-2] == piece and board[r-3][c-3] == piece:
                return True


# visually representing the board using pygame
# for each position in the matrix the board is either filled with an empty black circle, or a palyer/AI red/yellow circle
def draw_board(board):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE ))
            if board[r][c] == 0:
                pygame.draw.circle(screen, WHITE, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            else :
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)

    pygame.display.update()


# evaluate a 'window' of 4 locations in a row based on what pieces it contains
# the values used can be experimented with
def evaluate_window(window, piece):
    # by default the oponent is the player
    opponent_piece = PLAYER_PIECE

    # if we are checking from the player's perspective, then the oponent is AI
    if piece == PLAYER_PIECE:
        opponent_piece = AI_PIECE

    # initial score of a window is 0
    score = 0

    # based on how many friendly pieces there are in the window, we increase the score
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    # or decrese it if the oponent has 3 in a row
    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4 

    return score    


# scoring the overall attractiveness of a board after a piece has been droppped
def score_position(board, piece):

    score = 0

    # score center column --> we are prioritizing the central column because it provides more potential winning windows
    center_array = [int(i) for i in list(board[:,COLS//2])]
    center_count = center_array.count(piece)
    score += center_count * 6

    # below we go over every single window in different directions and adding up their values to the score
    # score horizontal
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLS - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    # score vertical
    for c in range(COLS):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROWS-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    # score positively sloped diagonals
    for r in range(3,ROWS):
        for c in range(COLS - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # score negatively sloped diagonals
    for r in range(3,ROWS):
        for c in range(3,COLS):
            window = [board[r-i][c-i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

# checking if the given turn or in other words node in the minimax tree is terminal
# a terminal node is player winning, AI winning or board being filled up
def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


# The algorithm calculating the best move to make given a depth of the search tree.
# Depth is how many layers algorithm scores boards. Complexity grows exponentially.
# Alpha and beta are best scores a side can achieve assuming the opponent makes the best play.
# More on alpha-beta pruning here: https://www.youtube.com/watch?v=l-hh51ncgDI.
# maximizing_palyer is a boolean value that tells whether we are maximizing or minimizing
# in this implementation, AI is maximizing.
def minimax(board, depth, alpha, beta, maximizing_player):

    # all valid locations on the board
    valid_locations = get_valid_locations(board)

    # boolean that tells if the current board is terminal
    is_terminal = is_terminal_node(board)

    # if the board is terminal or depth == 0
    # we score the win very high and a draw as 0
    if depth == 0 or is_terminal:
        if is_terminal: # winning move 
            if winning_move(board, AI_PIECE):
                return (None, 10000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000)
            else:
                return (None, 0)
        # if depth is zero, we simply score the current board
        else: # depth is zero
            return (None, score_position(board, AI_PIECE))

    # if the current board is not rerminal and we are maximizing
    if maximizing_player:

        # initial value is what we do not want - negative infinity
        value = -math.inf

        # this will be the optimal column. Initially it is random
        column = random.choice(valid_locations)

        # for every valid column, we simulate dropping a piece with the help of a board copy
        # and run the minimax on it with decresed depth and switched player
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            # recursive call
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            # if the score for this column is better than what we already have
            if new_score > value:
                value = new_score
                column = col
            # alpha is the best option we have overall
            alpha = max(value, alpha) 
            # if alpha (our current move) is greater (better) than beta (opponent's best move), then 
            # the oponent will never take it and we can prune this branch
            if alpha >= beta:
                break

        return column, value
    
    # same as above, but for the minimizing player
    else: # for thte minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(value, beta) 
            if alpha >= beta:
                break
        return column, value


# get all columns where a piece can be
def get_valid_locations(board):
    valid_locations = []
    
    for column in range(COLS):
        if is_valid_location(board, column):
            valid_locations.append(column)

    return valid_locations


# end the game which will close the window eventually
def end_game():
    global game_over
    game_over = True
    print(game_over)


# various state tracker variables taht use the above fucntions
# -------------------------------

# initializing the board
board = create_board()

# initially nobody has won yet
game_over = False

# initially the game is not over - this is used for GUI quirks
not_over = True

# initial turn is random
turn = random.randint(PLAYER_TURN, AI_TURN)

# Inicialização do pygame e configuração da tela
pygame.init()

# Configuração da tela
SQUARESIZE = 90
width = COLS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE
circle_radius = int(SQUARESIZE / 2 - 5)
size = (width, height)
screen = pygame.display.set_mode(size)

# Exibição do menu inicial
player_name, algorithm, ply_depth = show_menu_screen(screen)

# Converte a profundidade do ply para inteiro (se necessário)
ply_depth = int(ply_depth)

# Escolha do algoritmo de IA
use_alpha_beta = algorithm == "Alfa-beta"

# Fonte para mensagens
my_font = pygame.font.SysFont("monospace", 75)

# Inicialização do tabuleiro e jogo
board = create_board()
draw_board(board)
pygame.display.update()

game_over = False
not_over = True
turn = random.randint(PLAYER_TURN, AI_TURN)

# No início do jogo (exibição das configurações escolhidas)
print(f"Jogador: {player_name}")
print(f"Algoritmo: {algorithm}")
print(f"Profundidade escolhida (ply): {ply_depth}")

# Loop principal do jogo
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Movimento do mouse e ação do jogador
        if event.type == pygame.MOUSEMOTION and not_over:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            xpos = pygame.mouse.get_pos()[0]
            if turn == PLAYER_TURN:
                pygame.draw.circle(screen, RED, (xpos, int(SQUARESIZE / 2)), circle_radius)

        if event.type == pygame.MOUSEBUTTONDOWN and not_over:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

            if turn == PLAYER_TURN:
                xpos = event.pos[0]
                col = int(math.floor(xpos / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        print(f"{player_name.upper()} WINS!")
                        label = my_font.render(f"{player_name.upper()} WINS!", 1, RED)
                        screen.blit(label, (40, 10))
                        not_over = False
                        Timer(3.0, end_game).start()

                draw_board(board)
                turn = (turn + 1) % 2

        pygame.display.update()

    # Turno da IA
    if turn == AI_TURN and not game_over and not_over:
        start_time = time.time()  # Início do timer
        if use_alpha_beta:
            col, minimax_score = minimax(board, ply_depth, -math.inf, math.inf, True)
        else:
            col, minimax_score = minimax(board, ply_depth, -math.inf, math.inf, True)
        end_time = time.time()  # Fim do timer

        elapsed_time = end_time - start_time  # Tempo total decorrido

        if is_valid_location(board, col):
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                print("PLAYER 2 WINS!")
                label = my_font.render("PLAYER 2 WINS!", 1, YELLOW)
                screen.blit(label, (40, 10))
                not_over = False
                Timer(3.0, end_game).start()

        draw_board(board)

        # Logs no terminal
        print(f"IA escolheu a coluna: {col}")
        print(f"Tempo gasto pela IA: {elapsed_time:.4f} segundos")

        turn = (turn + 1) % 2