import pygame
import sys
from game import TicTacToe
from agent import QLearningAgent

WIDTH, HEIGHT = 500, 650
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS

CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

BG_COLOR = (28, 28, 30)
LINE_COLOR = (255, 255, 255)
CROSS_COLOR = (66, 133, 244)
CIRCLE_COLOR = (234, 67, 53)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (60, 60, 70)
BUTTON_HOVER = (80, 80, 90)
STATUS_BG = (40, 40, 45)  

STATUS_TOP = HEIGHT - 120   
SCORE_TOP = HEIGHT - 75   
BUTTON_TOP = HEIGHT - 40       
BUTTON_HEIGHT = 35


class TicTacToeInterface:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Крестики-нолики")
        
        self.font_status = pygame.font.SysFont('Arial', 32, bold=True)
        self.font_score = pygame.font.SysFont('Arial', 22)
        self.font_button = pygame.font.SysFont('Arial', 24, bold=True)
        
        self.game = TicTacToe()
        self.agent = QLearningAgent()
        
        if not self.agent.load_q_table("q_table.json"):
            print("Агент не обучен")
            pygame.quit()
            sys.exit()
        else:
            print(f"Агент загружен! Состояний: {len(self.agent.q_table)}")
        
        self.player_letter = 'X'
        self.ai_letter = 'O'
        
        self.game_over = False
        self.winner = None
        self.status_text = "Ваш ход"
        
        self.score = {'X': 0, 'O': 0, 'tie': 0}
        
        self.reset_button_rect = pygame.Rect(WIDTH//2 - 70, BUTTON_TOP, 140, BUTTON_HEIGHT)
        
        self.draw_status()
        
    def draw_board(self):
        self.screen.fill(BG_COLOR)
        
        for i in range(1, BOARD_ROWS):
            pygame.draw.line(self.screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)

        for i in range(1, BOARD_COLS):
            pygame.draw.line(self.screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, SQUARE_SIZE * BOARD_ROWS), LINE_WIDTH)
    
    def draw_figures(self):
        
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                index = row * 3 + col
                letter = self.game.board[index]
                
                x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                
                if letter == 'X':
                    offset = SQUARE_SIZE // 4
                    pygame.draw.line(self.screen, CROSS_COLOR, (x - offset, y - offset), (x + offset, y + offset), CROSS_WIDTH)
                    pygame.draw.line(self.screen, CROSS_COLOR, (x + offset, y - offset), (x - offset, y + offset), CROSS_WIDTH)
                elif letter == 'O':
                    pygame.draw.circle(self.screen, CIRCLE_COLOR, (x, y), CIRCLE_RADIUS, CIRCLE_WIDTH)
    
    def draw_status(self):
        
        self.draw_board()
        self.draw_figures()
        
        pygame.draw.rect(self.screen, STATUS_BG, (0, SQUARE_SIZE * BOARD_ROWS, WIDTH, HEIGHT - SQUARE_SIZE * BOARD_ROWS))
        
        status_surface = self.font_status.render(self.status_text, True, TEXT_COLOR)
        status_rect = status_surface.get_rect(center=(WIDTH//2, STATUS_TOP))
        self.screen.blit(status_surface, status_rect)
        
        score_text = f"X: {self.score['X']}   |   O: {self.score['O']}   |   Ничьи: {self.score['tie']}"
        score_surface = self.font_score.render(score_text, True, TEXT_COLOR)
        score_rect = score_surface.get_rect(center=(WIDTH//2, SCORE_TOP))
        self.screen.blit(score_surface, score_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        color = BUTTON_HOVER if self.reset_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        
        pygame.draw.rect(self.screen, color, self.reset_button_rect, border_radius=10)
        btn_text = self.font_button.render("Новая игра", True, TEXT_COLOR)
        btn_rect = btn_text.get_rect(center=self.reset_button_rect.center)
        self.screen.blit(btn_text, btn_rect)
        
        pygame.display.update()
    
    def reset_game(self):
        self.game.reset()
        self.game_over = False
        self.winner = None
        self.status_text = "Ваш ход"
        self.draw_status()
    
    def handle_click(self, pos):
        x, y = pos
        
        if self.reset_button_rect.collidepoint(pos):
            self.reset_game()
            return
        
        if self.game_over:
            return
        
        if y > SQUARE_SIZE * BOARD_ROWS:
            return
        
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        index = row * 3 + col
        
        if self.game.board[index] != ' ':
            return
        
        self.game.make_move(index, self.player_letter)
        
        if self.game.current_winner == self.player_letter:
            self.game_over = True
            self.score['X'] += 1
            self.status_text = "Вы победили"
            self.draw_status()
            return
        
        if self.game.num_empty_squares() == 0:
            self.game_over = True
            self.score['tie'] += 1
            self.status_text = "Ничья"
            self.draw_status()
            return
        
        self.status_text = "Компьютер думает..."
        self.draw_status()
        
        ai_move = self.agent.get_best_move(self.game.board)
        self.game.make_move(ai_move, self.ai_letter)
        
        if self.game.current_winner == self.ai_letter:
            self.game_over = True
            self.score['O'] += 1
            self.status_text = "Вы проиграли"
        elif self.game.num_empty_squares() == 0:
            self.game_over = True
            self.score['tie'] += 1
            self.status_text = "Ничья"
        else:
            self.status_text = "Ваш ход"
        
        self.draw_status()
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.MOUSEMOTION:

                    self.draw_status()
            
            clock.tick(60)
        
        pygame.quit()
        sys.exit()