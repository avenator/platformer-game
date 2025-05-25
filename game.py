import pygame
import time

pygame.font.init()

# === Константы ===
FONT_PATH = "fonts/maturamtscriptcapitals.ttf"
LIFE_IMAGE_PATH = "assets/life/life.png"
COLOR_MESSAGE = pygame.Color("darkorange")
COLOR_CRIMSON = "crimson"
COLOR_GREEN = "green"
COLOR_RED = "red"
COLOR_BLACK = "black"
COLOR_WHITE = "white"

class Game:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height

        self.font_large = pygame.font.Font(FONT_PATH, 300)
        self.font_medium = pygame.font.Font(FONT_PATH, 150)
        self.font_small = pygame.font.Font(FONT_PATH, 75)
        self.status_font = pygame.font.SysFont('bloodcyrillic', 100)

        self.message_color = COLOR_MESSAGE
        self.pygame_rect = pygame.Rect(1770, 0, 150, 150)

    def _game_lose(self, player):
        player.game_over = True
        message = self.font_medium.render('- 10 points', True, self.message_color)
        self.screen.blit(message, (self.WIDTH // 3 + 70, 70))
        pygame.display.update()

    def _game_respawn(self, player, player2):
        player2.points = max(player2.points - 10, 0)
        if player2.jump in player2.jumps:
            player2.jump += 1

        self.screen.fill(COLOR_BLACK)
        fail_message = self.font_large.render('Failed', True, COLOR_CRIMSON)
        self.screen.blit(fail_message, (self.WIDTH // 6, 350))

        jump_is_new = (player2.jump - 1 not in player2.jumps)
        player_fell = player.rect.y >= self.HEIGHT - 30
        player2_safe = player2.rect.y < self.HEIGHT - 30

        self._draw_respawn_effect(jump_is_new, player_fell, player2_safe)

    def _draw_respawn_effect(self, new_jump, player_fell, player2_safe):
        sequence = [1000, 9000] if new_jump and player_fell and player2_safe else \
                   [1000, 1000, 1000, 7000] if new_jump else \
                   [1000, 9000]

        for i, delay in enumerate(sequence):
            color = COLOR_WHITE if i % 2 == 0 else COLOR_BLACK
            pygame.draw.rect(self.screen, color, self.pygame_rect)
            pygame.display.update()
            pygame.time.delay(delay)

    def _game_win(self, player):
        message = self.font_medium.render('+ 50 points', True, self.message_color)
        player.points += 50
        self.screen.blit(message, (self.WIDTH // 4, 170))
        pygame.display.update()

    def game_over(self):
        self.screen.fill(COLOR_BLACK)
        message = self.font_large.render('Game over!', True, COLOR_CRIMSON)
        self.screen.blit(message, (self.WIDTH // 8, 350))
        pygame.display.update()
        pygame.time.delay(10000)

    def ai_state(self, player, player2, level=0):
        if player.rect.y >= self.HEIGHT - 30 and level > -1:
            self._game_respawn(player, player2)
            return 'respawn'
        return None

    def game_state(self, player, player2, goal, level=0):
        if player2.rect.y >= self.HEIGHT and level > -1:
            self._game_respawn(player, player2)
            return 'respawn'
        elif player2.rect.colliderect(goal.rect):
            return 'next'
        return None

    def show_life(self, player):
        life_image = pygame.image.load(LIFE_IMAGE_PATH)
        life_image = pygame.transform.scale(life_image, (30, 30))
        for i in range(player.life):
            self.screen.blit(life_image, ((i + 1) * 30, 30))

    def show_score(self, player):
        message = self.font_small.render(f'Score: {player.points}', True, COLOR_BLACK)
        self.screen.blit(message, (500, 1))

    def show_level(self, player):
        message = self.font_medium.render(f'Level: {player.level + 1}', True, self.message_color)
        self.screen.blit(message, (500, 1))

    def show_jumps(self, player):
        message = self.font_medium.render(f'Jump: {player.jump}', True, self.message_color)
        self.screen.blit(message, (500, 1))

    def show_online(self):
        message = self.font_small.render('Online', True, COLOR_GREEN)
        self.screen.blit(message, (1, 1))

    def show_train(self):
        message = self.font_small.render('Training', True, COLOR_GREEN)
        self.screen.blit(message, (1, 1))

    def show_offline(self):
        message = self.font_small.render('Offline', True, COLOR_RED)
        self.screen.blit(message, (1, 1))
