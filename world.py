import pygame
import time

from settings import tile_size
from tile import Tile
from trap import Trap
from goal import Goal
from player import Player
from game import Game
from coin import Coin

class World:
    def __init__(self, world_data, screen, width, height):
        self.screen = screen
        self.first = True
        self.world_data = world_data
        self._setup_world(world_data)
        self.world_shift = 0
        self.current_x = 0
        self.gravity = 0.7
        self.WIDTH = width
        self.HEIGHT = height
        self.game = Game(self.screen, width, height)

    def _setup_world(self, layout):
        self.tiles = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.player1 = pygame.sprite.GroupSingle()
        self.player2 = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x, y = col_index * tile_size, row_index * tile_size

                if cell == "X":
                    self.tiles.add(Tile((x, y), tile_size))
                elif cell == "t":
                    self.traps.add(Trap((x + tile_size // 4, y + tile_size // 4), tile_size // 2))
                elif cell == "P":
                    player2 = Player((x, y), ai=False)
                    self.player2.start = (x, y)
                    self.player2.add(player2)
                elif cell == "c":
                    self.coins.add(Coin((x + tile_size // 4, y + tile_size // 4), tile_size // 2))
                elif cell == "I":
                    player1 = Player((x, y), ai=True)
                    self.player1.start = (x, y)
                    self.player1.add(player1)
                elif cell == "G":
                    self.goal.add(Goal((x, y), tile_size))

    def _scroll_x(self, player_group):
        player = player_group.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < self.WIDTH // 3 and direction_x < 0:
            self.world_shift = 4
            player.speed = 0
        elif player_x > self.WIDTH - self.WIDTH // 3 and direction_x > 0:
            self.world_shift = -4
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 3

    def _apply_gravity(self, player):
        player.direction.y += self.gravity
        player.rect.y += player.direction.y

    def _horizontal_movement_collision(self, player_group):
        player = player_group.sprite
        player.rect.x += player.direction.x * player.speed

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = tile.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = tile.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def _vertical_movement_collision(self, player_group):
        player = player_group.sprite
        self._apply_gravity(player)

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = tile.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = tile.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and (player.direction.y < 0 or player.direction.y > 1):
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def _handle_traps(self, player_group):
        player = player_group.sprite

        for trap in self.traps.sprites():
            if trap.rect.colliderect(player.rect):
                if player.direction.x != 0 or player.direction.y > 0:
                    offset = tile_size if player.direction.x < 0 else -tile_size
                    player.rect.x += offset
                player.life -= 1

    def _handle_coins(self, player_group):
        player = player_group.sprite

        for coin in self.coins.sprites():
            if coin.rect.colliderect(player.rect):
                player.points += 10
                coin.kill()

    def update(self, player_event, timer, level, ai_event=None):
        self.tiles.draw(self.screen)
        self.traps.update(self.world_shift)
        self.traps.draw(self.screen)
        self.coins.update(self.world_shift)
        self.coins.draw(self.screen)
        self.goal.update(self.world_shift)
        self.goal.draw(self.screen)

        self.player1.update(ai_event)
        self.player2.update(player_event)

        self._horizontal_movement_collision(self.player1)
        self._horizontal_movement_collision(self.player2)
        self._vertical_movement_collision(self.player1)
        self._vertical_movement_collision(self.player2)
        self._handle_coins(self.player2)

        if level > -1:
            self.game.show_score(self.player2.sprite)
        else:
            self.game.show_train()

        if level > -1:
            if time.process_time() - timer > 1:
                self.game.show_online()
            else:
                self.game.show_offline()

        if level > -1 and time.process_time() - timer > 1:
            self.player1.draw(self.screen)

        self.player2.draw(self.screen)

        state = self.game.game_state(self.player1.sprite, self.player2.sprite, self.goal.sprite, level)
        state2 = self.game.ai_state(self.player1.sprite, self.player2.sprite, level)

        if state2 == 'respawn':
            self.player2.sprite.points = max(0, self.player2.sprite.points - 10)
            if self.player2.sprite.jump in self.player2.sprite.jumps:
                self.player2.sprite.jump += 1

        return state, state2