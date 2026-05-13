import numpy as np
import random
import pygame
import sys

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Font
FONT = pygame.font.Font(None, 36)
SMALL_FONT = pygame.font.Font(None, 24)


class TicTacToeGame:
    def __init__(self, size=3, difficulty=3, vs_ai=False):
        self.size = size
        self.difficulty = difficulty
        self.vs_ai = vs_ai
        self.ai_player = 'O' if random.choice([True, False]) else 'X'  # AI plays as random player
        self.cell_size = 100
        self.margin = 50
        self.screen_width = self.size * self.cell_size + 2 * self.margin
        self.screen_height = self.size * self.cell_size + 2 * self.margin + 100  # Extra space for status
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tic Tac Toe")
        self.board = self.create_board()
        self.turn = 'X'  # Human always starts as X
        self.game_over = False
        self.winner = None
        self.ai_thinking = False

    def create_board(self):
        return np.array([[' '] * self.size] * self.size)

    def draw_board(self):
        self.screen.fill(WHITE)
        
        # Draw grid lines
        for i in range(1, self.size):
            # Vertical lines
            pygame.draw.line(self.screen, BLACK, 
                           (self.margin + i * self.cell_size, self.margin), 
                           (self.margin + i * self.cell_size, self.margin + self.size * self.cell_size), 3)
            # Horizontal lines
            pygame.draw.line(self.screen, BLACK, 
                           (self.margin, self.margin + i * self.cell_size), 
                           (self.margin + self.size * self.cell_size, self.margin + i * self.cell_size), 3)

        # Draw X and O
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row, col] == 'X':
                    self.draw_x(row, col)
                elif self.board[row, col] == 'O':
                    self.draw_o(row, col)

        # Draw status
        status_text = f"Player {self.turn}'s turn"
        if se>lf.ai_thinking:
            status_text = "AI is thinking..."
        if self.game_over:
            if self.winner:
                status_text = f"Player {self.winner} wins!"
            else:
                status_text = "It's a tie!"
        
        text = FONT.render(status_text, True, BLACK)
        self.screen.blit(text, (self.margin, self.margin + self.size * self.cell_size + 20))

        # Draw restart button
        mode_text = "Mode: " + ("vs AI" if self.vs_ai else "vs Player")
        mode_render = SMALL_FONT.render(mode_text, True, BLACK)
        self.screen.blit(mode_render, (self.margin, self.margin + self.size * self.cell_size + 45))
        
        restart_text = SMALL_FONT.render("R: restart, S: settings, M: change mode", True, BLACK)
        self.screen.blit(restart_text, (self.margin, self.margin + self.size * self.cell_size + 65))

    def draw_x(self, row, col):
        center_x = self.margin + col * self.cell_size + self.cell_size // 2
        center_y = self.margin + row * self.cell_size + self.cell_size // 2
        offset = self.cell_size // 4
        pygame.draw.line(self.screen, RED, (center_x - offset, center_y - offset), 
                        (center_x + offset, center_y + offset), 5)
        pygame.draw.line(self.screen, RED, (center_x + offset, center_y - offset), 
                        (center_x - offset, center_y + offset), 5)

    def draw_o(self, row, col):
        center_x = self.margin + col * self.cell_size + self.cell_size // 2
        center_y = self.margin + row * self.cell_size + self.cell_size // 2
        radius = self.cell_size // 4
        pygame.draw.circle(self.screen, BLUE, (center_x, center_y), radius, 5)

    def get_cell_from_pos(self, pos):
        x, y = pos
        if self.margin <= x <= self.margin + self.size * self.cell_size and \
           self.margin <= y <= self.margin + self.size * self.cell_size:
            col = (x - self.margin) // self.cell_size
            row = (y - self.margin) // self.cell_size
            return row, col
        return None

    def make_move(self, row, col):
        if not self.game_over and self.board[row, col] == ' ':
            self.board[row, col] = self.turn
            if self.check_win(self.turn):
                self.game_over = True
                self.winner = self.turn
            elif self.is_board_full():
                self.game_over = True
                self.winner = None
            else:
                self.turn = 'O' if self.turn == 'X' else 'X'

    def check_win(self, player):
        # Check rows
        for row in self.board:
            if player * self.difficulty in ''.join(row):
                return True
        # Check columns
        for i in range(self.size):
            if player * self.difficulty in ''.join(self.board[:, i]):
                return True
        # Check diagonals
        for offset in range(-self.size + 1, self.size):
            if player * self.difficulty in ''.join(self.board.diagonal(offset)):
                return True
        for offset in range(-self.size + 1, self.size):
            if player * self.difficulty in ''.join(np.flipud(self.board).diagonal(offset)):
                return True
        return False

    def is_board_full(self):
        return not (' ' in self.board)

    def restart_game(self):
        self.board = self.create_board()
        self.turn = random.choice(['O', 'X'])
        self.game_over = False
        self.winner = None

    def toggle_mode(self):
        self.vs_ai = not self.vs_ai
        if self.vs_ai:
            self.ai_player = 'O' if random.choice([True, False]) else 'X'
        self.restart_game()

    def minimax(self, board, depth, is_maximizing, alpha=-float('inf'), beta=float('inf')):
        if self.check_win(self.ai_player):
            return 10 - depth
        elif self.check_win('X' if self.ai_player == 'O' else 'O'):
            return depth - 10
        elif self.is_board_full():
            return 0

        if is_maximizing:
            max_eval = -float('inf')
            for row in range(self.size):
                for col in range(self.size):
                    if board[row, col] == ' ':
                        board[row, col] = self.ai_player
                        eval = self.minimax(board, depth + 1, False, alpha, beta)
                        board[row, col] = ' '
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = float('inf')
            opponent = 'X' if self.ai_player == 'O' else 'O'
            for row in range(self.size):
                for col in range(self.size):
                    if board[row, col] == ' ':
                        board[row, col] = opponent
                        eval = self.minimax(board, depth + 1, True, alpha, beta)
                        board[row, col] = ' '
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval

    def get_best_move(self):
        best_score = -float('inf')
        best_move = None
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row, col] == ' ':
                    self.board[row, col] = self.ai_player
                    score = self.minimax(self.board, 0, False)
                    self.board[row, col] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        return best_move

    def ai_move(self):
        if not self.game_over and self.vs_ai and self.turn == self.ai_player:
            self.ai_thinking = True
            pygame.display.flip()  # Update display to show thinking
            move = self.get_best_move()
            if move:
                self.make_move(*move)
            self.ai_thinking = False

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over and not self.ai_thinking:
                    if not self.vs_ai or self.turn != self.ai_player:
                        cell = self.get_cell_from_pos(event.pos)
                        if cell:
                            self.make_move(*cell)
                            if self.vs_ai and not self.game_over:
                                self.ai_move()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart_game()
                    elif event.key == pygame.K_s:
                        self.change_settings()
                    elif event.key == pygame.K_m:
                        self.toggle_mode()
                    elif event.key == pygame.K_q:
                        running = False

            self.draw_board()
            pygame.display.flip()

        pygame.quit()
        sys.exit()


def main():
    game = TicTacToeGame(vs_ai=True)
    game.run()


if __name__ == "__main__":
    main()
