# importing important packages:
import copy
import sys
import pygame
import random
import numpy as np


# declaring variables for board:
width = 800
height = 800
rows = 3
columns = 3
squareSize = width // columns
lwidth = 15
circleWidth = 15
crossWidth = 20
radius = squareSize // 4
offset = 50
bg_colour = (49,50,49)
line_colour =(89, 89, 89)
circle_colour = (51, 204, 136)
cross_colour =( 231, 89, 24)    


# initialized the game using pygame:
pygame.init()
screen = pygame.display.set_mode( (width, height) )
pygame.display.set_caption('Tic-Tac-Toe AI Project')
screen.fill( bg_colour)

class Conditions:

    def __init__(self):
        self.squares = np.zeros( (rows, columns) )     # creating a empty 2d 3x3 array
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0

    # for eval function: 
    # return 0 if there is no win yet
    # return 1 if player 1 wins
    # return 2 if player 2 wins
        
    def final_state(self, show=False):

        
        # vertical wins
        for col in range(columns):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = circle_colour if self.squares[0][col] == 2 else cross_colour
                    ini_position = (col * squareSize + squareSize // 2, 20)
                    final_position = (col * squareSize + squareSize // 2, height - 20)
                    pygame.draw.line(screen, color, ini_position, final_position, lwidth)
                return self.squares[0][col]

        # horizontal wins
        for row in range(rows):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = circle_colour if self.squares[row][0] == 2 else cross_colour
                    ini_position = (20, row * squareSize + squareSize // 2)
                    final_position = (width - 20, row * squareSize + squareSize // 2)
                    pygame.draw.line(screen, color, ini_position, final_position, lwidth)
                return self.squares[row][0]

        # \ diagonal wins
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = circle_colour if self.squares[1][1] == 2 else cross_colour
                ini_position = (20, 20)
                final_position = (width - 20, height - 20)
                pygame.draw.line(screen, color, ini_position, final_position, crossWidth)
            return self.squares[1][1]

        # / diagonal wins
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = circle_colour if self.squares[1][1] == 2 else cross_colour
                ini_position = (20, height - 20)
                final_position = (width - 20, 20)
                pygame.draw.line(screen, color, ini_position, final_position, crossWidth)
            return self.squares[1][1]

        # if no win yet
        return 0

    # marking squares :
    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    # checking for no. of empty squares which will be used in the minmax algorithm:
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(rows):
            for col in range(columns):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col) )
        
        return empty_sqrs

    # checking for draw:
    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0

class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    # To choose random squares by ai:
    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))
        return empty_sqrs[idx]
    
    # Minmax algo:
    def minmax(self, board, maximizing):
        
        case = board.final_state()  

        # player 1 wins
        if case == 1:
            return 1, None

        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minmax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minmax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    # eval fn:
    def eval(self, main_board):
        if self.level == 0:
            # setting eval = random :
            eval = 'random'
            move = self.rnd(main_board)
        else:
            # minmax algo choice
            eval, move = self.minmax(main_board, False)

        # print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')

        return move # row, col

class Game:

    def __init__(self):
        self.board = Conditions()
        self.ai = AI()
        self.player = 1   #1-cross  #2-circles
        self.gamemode = 'ai' # pvp or ai
        self.running = True
        self.show_lines()

    # --- DRAW METHODS ---

    def show_lines(self):
        # bg
        screen.fill( bg_colour )

        # vertical
        pygame.draw.line(screen, line_colour, (squareSize, 0), (squareSize, height), lwidth)
        pygame.draw.line(screen, line_colour, (width - squareSize, 0), (width - squareSize, height), lwidth)

        # horizontal
        pygame.draw.line(screen, line_colour, (0, squareSize), (width, squareSize), lwidth)
        pygame.draw.line(screen, line_colour, (0, height - squareSize), (width, height - squareSize), lwidth)

    def draw_fig(self, row, col):
        if self.player == 1:
            # draw cross
            # desc line
            start_desc = (col * squareSize + offset, row * squareSize + offset)
            end_desc = (col * squareSize + squareSize - offset, row * squareSize + squareSize - offset)
            pygame.draw.line(screen, cross_colour, start_desc, end_desc, crossWidth)
            # asc line
            start_asc = (col * squareSize + offset, row * squareSize + squareSize - offset)
            end_asc = (col * squareSize + squareSize - offset, row * squareSize + offset)
            pygame.draw.line(screen, cross_colour, start_asc, end_asc, crossWidth)
        
        elif self.player == 2:
            # draw circle
            center = (col * squareSize + squareSize // 2, row * squareSize + squareSize // 2)
            pygame.draw.circle(screen, circle_colour, center, radius, circleWidth)

    # --- OTHER METHODS ---

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

def display_message_box(message):
    box_width = 600
    box_height = 100
    box_color = (255, 255, 255)
    text_color = (0,0,0)
    font = pygame.font.Font(None, 24)

    message_box = pygame.Surface((box_width, box_height))
    message_box.fill(box_color)

    text = font.render(message, True, text_color)
    text_rect = text.get_rect(center=(box_width // 2, box_height // 2))
    message_box.blit(text, text_rect)

    screen_rect = screen.get_rect()
    screen.blit(message_box, (screen_rect.centerx - box_width // 2, screen_rect.centery - box_height // 2))

    pygame.display.update()

def main():

    # --- OBJECTS ---

    game = Game()
    board = game.board
    ai = game.ai

    # --- MAINLOOP ---

    while True:
        
        # pygame events
        for event in pygame.event.get():

            # quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # keydown event
            if event.type == pygame.KEYDOWN:

                # g-gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # r-restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                # 0-random ai
                if event.key == pygame.K_0:
                    ai.level = 0
                
                # 1-random ai
                if event.key == pygame.K_1:
                    ai.level = 1

            # click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // squareSize
                col = pos[0] // squareSize
                
                # human mark sqr
                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False


        # AI initial call
        if game.gamemode == 'ai' and game.player == ai.player and game.running:

            # update the screen
            pygame.display.update()

            # eval
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False
                message = "Press R to restart, G to play 1v1, 0 for easy mode, and 1 for hard"
                display_message_box(message)

            
        pygame.display.update()

main()