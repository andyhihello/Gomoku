import pygame
import numpy as np

# 定義顏色常數
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Game:
    def __init__(self, n=16):
        self.n = n
        self.board = np.zeros((n, n))
        self.current_player = 1
        self.is_over = False
        self.winner = None
        
    def play(self, x, y):
        if x > 15 or y > 15:
            return False
        elif self.board[x][y] != 0 or self.is_over:
            return False
        
        self.board[x][y] = self.current_player
        self.current_player = 3 - self.current_player
        
        self.is_over, self.winner = self.check_win(x, y)
        
        return True
    
    def check_win(self, x, y):
        player = self.board[x][y]
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            for k in range(1, 5):
                nx, ny = x + k * dx, y + k * dy
                if 0 <= nx < self.n and 0 <= ny < self.n and self.board[nx][ny] == player:
                    count += 1
                else:
                    break
            for k in range(1, 5):
                nx, ny = x - k * dx, y - k * dy
                if 0 <= nx < self.n and 0 <= ny < self.n and self.board[nx][ny] == player:
                    count += 1
                else:
                    break
            if count >= 5:
                return True, player
        return False, None

class GUI:
    def __init__(self, game):
        self.game = game
        self.width = 640
        self.height = 760
        self.cell_size = self.width // self.game.n
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.font.init()
        self.font_path = 'C:\Windows\Fonts\kaiu.ttf'
        self.font = pygame.font.Font(self.font_path, 40)
        self.game_over = False
        self.undo_button_rect = pygame.Rect(560,630,self.width,self.height)
        

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    i, j = y // self.cell_size, x // self.cell_size
                    if self.game.play(i, j):
                        self.draw_board()
                        if self.game.is_over:
                            self.game_over = True 
                    if self.undo_button_rect.collidepoint(x, y): 
                        print('hihello')
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: 
                        self.reset_game()
                
            self.draw_board()
            self.undo_botton()
            if self.game_over:
                self.show_result()
            pygame.display.flip()
            
    def draw_board(self):
        backgroud_image = pygame.image.load("background.jpg")
        background_rect = pygame.Rect(0,0,self.width,self.height)
        pygame.draw.rect(self.screen,(0,0,0),background_rect)
        self.screen.blit(backgroud_image,background_rect)

        for i in range(self.game.n):
            pygame.draw.line(self.screen, BLACK, (self.cell_size // 2, i * self.cell_size + self.cell_size // 2), 
                             (self.width - self.cell_size // 2, i * self.cell_size + self.cell_size // 2), 2)
            pygame.draw.line(self.screen, BLACK, (i * self.cell_size + self.cell_size // 2, self.cell_size // 2), 
                             (i * self.cell_size + self.cell_size // 2, self.height - self.cell_size // 2-120), 2)
        for i in range(self.game.n):
            for j in range(self.game.n):
                if self.game.board[i][j] == 1:
                    pygame.draw.circle(self.screen, RED, (j * self.cell_size + self.cell_size // 2, i * self.cell_size + self.cell_size // 2), 
                               self.cell_size // 2.7, 0)
                    pygame.draw.circle(self.screen, BLACK, (j * self.cell_size + self.cell_size // 2, i * self.cell_size + self.cell_size // 2), 
                               self.cell_size // 2.7, 1)
                elif self.game.board[i][j] == 2:
                    pygame.draw.circle(self.screen, BLUE, (j * self.cell_size + self.cell_size // 2, i * self.cell_size + self.cell_size // 2), 
                               self.cell_size // 2.7, 0)
                    pygame.draw.circle(self.screen, BLACK, (j * self.cell_size + self.cell_size // 2, i * self.cell_size + self.cell_size // 2), 
                               self.cell_size // 2.7, 1)
    def undo_botton(self):
        undo_image = pygame.image.load("undo.jpg")
        self.screen.blit(undo_image, self.undo_button_rect) 

    def show_result(self):
        if self.game.winner == 1:
            text = self.font.render('Red player wins!', True, RED)
        elif self.game.winner == 2:
            text = self.font.render('Blue player wins!', True, BLUE)
        else:
            text = self.font.render('Tie game!', True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (self.width // 2, self.height // 10 * 8.5)
        self.screen.blit(text, text_rect)

        text_restart = self.font.render("Press R to restart", True,BLACK)
        text_restart_rect = text.get_rect()
        text_restart_rect.center = (self.width // 2.1, self.height // 10 * 9)
        self.screen.blit(text_restart,text_restart_rect)

    def reset_game(self):
        self.game = Game()
        self.game_over = False
        self.draw_board()
        pygame.display.flip()
        

pygame.init()
gui = GUI(Game())
gui.run()
