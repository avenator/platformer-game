import os
import sys
import time
import pygame
import pandas as pd
import pygame_textinput

from settings import *
from world import World
from pool import pool

# === Константы ===
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (220, 200, 0)
RANGES = [[i, i + 150] for i in range(50, 3350, 150)]

# === Инициализация ===
pygame.init()
pygame.display.set_caption("Platformer")


class Platformer:
    def __init__(self, subject_name):
        self.subject_name = subject_name
        self.level = 0
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.WIDTH, self.HEIGHT = self.screen.get_size()

        self.player_event = False
        self.state = None
        self.points = 0
        self.glevel = -2
        self.gjump = 0
        self.pygame_rect = pygame.Rect(1770, 0, 150, 150)
        self.dcts = []

        # Фон
        self.images = os.listdir('assets/terrain/background')
        self.bg_img = pygame.image.load('assets/terrain/background/1.jpg')
        self.bg_img = pygame.transform.scale(self.bg_img, (self.WIDTH, self.HEIGHT))

    def respawn(self, player):
        for r in RANGES:
            if r[0] <= player.sprite.rect.x < r[1]:
                player.sprite.rect.x = r[0]
        player.sprite.rect.y = 300

    def respawn_to_start(self, player):
        player.sprite.rect.x, player.sprite.rect.y = player.start

    def update_screen(self):
        self.WIDTH, self.HEIGHT = pygame.display.get_surface().get_size()
        self.bg_img = pygame.transform.scale(self.bg_img, (self.WIDTH, self.HEIGHT))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def main(self, timer):
        tim = timer
        self.update_screen()
        self.world = World(world_map[self.glevel], self.screen, self.WIDTH, self.HEIGHT)

        player2 = self.world.player2.sprite
        player2.points = self.points
        player2.jump = self.gjump
        player2.level = self.glevel

        self.bg_img = pygame.image.load(f'assets/terrain/background/{self.images[self.glevel]}')
        self.bg_img = pygame.transform.scale(self.bg_img, (self.WIDTH, self.HEIGHT))

        self.ai_event = None
        fail_jump = False
        steps = 0

        while True:
            steps += 1
            self.screen.blit(self.bg_img, (0, 0))
            self.ai_event = self._calculate_ai_event(fail_jump, steps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    self._handle_keydown(event.key, tim)

                elif event.type == pygame.KEYUP:
                    self.player_event = False

            state, state2 = self.world.update(
                player_event=self.player_event,
                ai_event=self.ai_event,
                timer=tim,
                level=self.glevel
            )

            if self.world.player2.sprite.jump > 305:
                self.world.game.game_over()
                self._log_event('end')
                return 'end', tim

            if any(s == 'respawn' for s in (state, state2)) or state in ('next', 'restart'):
                break

            if state2 == 'respawn':
                self.respawn_to_start(self.world.player1)

            pygame.draw.rect(self.screen, COLOR_BLACK, self.pygame_rect)
            pygame.display.update()
            self.clock.tick(60)

        return self._handle_state_transition(state, state2, tim)

    def _calculate_ai_event(self, fail_jump, steps):
        player1 = self.world.player1.sprite
        player2 = self.world.player2.sprite

        if self.glevel > -1:
            if abs(player1.rect.x + 5) < player2.rect.x:
                return 'right' if player1.rect.y <= 450 else 'space'
            if abs(player1.rect.x + 5) > player2.rect.x:
                return 'left' if player1.rect.y <= 450 else 'space'
            if player1.rect.x == player2.rect.x:
                return None
            if player2.jump_fail():
                if not fail_jump:
                    return 'space'
                elif steps < 50:
                    return 'right'
                else:
                    return None
        return None

    def _handle_keydown(self, key, tim):
        if key == pygame.K_LEFT:
            self.player_event = "left"
        elif key == pygame.K_RIGHT:
            self.player_event = "right"
        elif key == pygame.K_UP:
            self.world.player2.sprite.jump += 1
            self.player_event = "space"
        elif key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif key == pygame.K_2:
            self._log_event('start')
            df = pd.DataFrame(self.dcts)
            df.to_excel(f'{self.subject_name}.xlsx')
            self._reset_game()
            return 'restart', time.process_time()
        elif key == pygame.K_1:
            self.glevel = -2
            return 'restart', tim

    def _handle_state_transition(self, state, state2, tim):
        if state == 'next':
            self.glevel = (self.glevel + 1) % 6 if self.glevel > -1 else -2
            self.gjump = self.world.player2.sprite.jump
            self.points = self.world.player2.sprite.points
            return 'restart', tim

        if state in ('restart', 'respawn') or state2 == 'respawn':
            self._log_respawn_event(state, state2)
            self.points = 0
            self.glevel = -2 if self.glevel < 0 else 0
            self.gjump = self.world.player2.sprite.jump
            return 'restart', tim

        return 'end', tim

    def _reset_game(self):
        self.glevel = 0
        self.gjump = 0
        self.points = 0
        self.world.player2.sprite.jump = 0

    def _log_event(self, event_type):
        self.dcts.append(pool(event_type))
        df = pd.DataFrame(self.dcts)
        df.to_excel(f'{self.subject_name}.xlsx')

    def _log_respawn_event(self, state, state2):
        if self.glevel > -1:
            if state == 'respawn':
                self.dcts.append(pool('player', jump=self.gjump))
            elif state2 == 'respawn' and state != 'respawn':
                self.dcts.append(pool('ai', jump=self.gjump - 1))
            df = pd.DataFrame(self.dcts)
            df.to_excel(f'{self.subject_name}.xlsx')


def get_subject_name():
    textinput = pygame_textinput.TextInputVisualizer()
    screen = pygame.display.set_mode((1000, 200))
    pygame.display.set_caption("Enter Subject name")
    clock = pygame.time.Clock()

    while True:
        screen.fill((225, 225, 225))
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                return textinput.value

        textinput.update(events)
        screen.blit(textinput.surface, (10, 10))
        pygame.display.update()
        clock.tick(30)

        if pygame.key.get_pressed()[pygame.K_RETURN]:
            return textinput.value


if __name__ == "__main__":
    subject_name = get_subject_name()
    play = Platformer(subject_name=subject_name)
    t = time.process_time()

    while True:
        state, t = play.main(timer=t)
        if state != 'restart':
            break
