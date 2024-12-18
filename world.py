import pygame
from settings import tile_size
from tile import Tile
from trap import Trap
from goal import Goal
from player import Player
from game import Game
from coin import Coin
from pool import pool
import time
from support import find_node, find_path
class World:
	def __init__(self, world_data, screen, WIDTH, HEIGHT):
		self.screen = screen
		self.first = True
		self.world_data = world_data
		self._setup_world(world_data)
		self.world_shift = 0
		self.current_x = 0
		self.gravity = 0.7
		self.WIDTH = WIDTH
		self.HEIGHT = HEIGHT
		self.game = Game(self.screen, WIDTH, HEIGHT)


	# generates the world
	def _setup_world(self, layout):
		self.tiles = pygame.sprite.Group()
		self.traps = pygame.sprite.Group()
		self.coins = pygame.sprite.Group()
		self.player1 = pygame.sprite.GroupSingle()
		self.player2 = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.checkpoints = []
		for row_index, row in enumerate(layout):
			for col_index, cell in enumerate(row):
				x, y = col_index * tile_size, row_index * tile_size
				if cell == "X":
					tile = Tile((x, y), tile_size)
					#print(x, y)
					self.tiles.add(tile)
				elif cell == "t":
					tile = Trap((x + (tile_size // 4), y + (tile_size // 4)), tile_size // 2)
					self.traps.add(tile)
				elif cell == "P":
					player2_sprite = Player((x, y), ai=False)
					player2_sprite.ai = False
					self.player2.start = (x, y)
					self.player2.add(player2_sprite)
				elif cell == 'c':
					tile = Coin((x + (tile_size // 4), y + (tile_size // 4)), tile_size // 2)
					self.coins.add(tile)
				elif cell == 'I':
					player1_sprite = Player((x, y), ai=True)
					#print(x, y)
					player1_sprite.ai = True
					self.player1.start = (x, y)
					self.player1.add(player1_sprite)

				elif cell == "G":
					self.g = x, y
					goal_sprite = Goal((x, y), tile_size)
					self.goal.add(goal_sprite)

	# world scroll when the player2_2 is walking towards left/right
	def _scroll_x(self, player):
		player = player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < self.WIDTH // 3 and direction_x < 0:
			self.world_shift = 4
			player.speed = 0
		elif player_x > self.WIDTH - (self.WIDTH // 3) and direction_x > 0:
			self.world_shift = -4
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 3

	# add gravity for player2_2 to fall
	def _apply_gravity(self, player):
		player.direction.y += self.gravity
		player.rect.y += player.direction.y

	# prevents player2_2 to pass through objects horizontally
	def _horizontal_movement_collision(self, player):
		player = player.sprite
		player.rect.x += player.direction.x * player.speed

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				# checks if moving towards left
				if player.direction.x < 0:
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				# checks if moving towards right
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right
		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False

	# prevents player2_2 to pass through objects vertically
	def _vertical_movement_collision(self, player):
		player = player.sprite
		self._apply_gravity(player)

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				# checks if moving towards bottom
				if player.direction.y > 0:
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				# checks if moving towards up
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True
		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0:
			player.on_ceiling = False

	# add consequences when player2_2 run through traps
	def _handle_traps(self, player):
		player = player.sprite

		for sprite in self.traps.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0 or player.direction.y > 0:
					player.rect.x += tile_size
				elif player.direction.x > 0 or player.direction.y > 0:
					player.rect.x -= tile_size
				player.life -= 1
	def _handle_coins(self, player):
		player = player.sprite
		for sprite in self.coins.sprites():
			if sprite.rect.colliderect(player.rect):
				player.points += 10
				sprite.kill()


	# updating the game world from all changes commited
	def update(self, player_event, timer, level, ai_event=None):
		# for tile
		#self.tiles.update(self.world_shift)
		self.tiles.draw(self.screen)

		# for trap
		self.traps.update(self.world_shift)
		self.traps.draw(self.screen)
		# for coins
		self.coins.update(self.world_shift)
		self.coins.draw(self.screen)
		# for goal
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
			self.game.show_train(self.player2.sprite)
		if level > -1:
			if time.process_time() - timer > 1:
						self.game.show_online(self.player2.sprite)
			if time.process_time() - timer < 1:
						self.game.show_offline(self.player2.sprite)
		if level > -1 and time.process_time() - timer > 1:
			self.player1.draw(self.screen)
		self.player2.draw(self.screen)
		state = self.game.game_state(self.player1.sprite, self.player2.sprite, self.goal.sprite, level=level)
		state2 = self.game.ai_state(self.player1.sprite, self.player2.sprite, level=level)
		if state2 == 'respawn':
			self.player2.sprite.points -= 10
			if self.player2.sprite.points < 0:
				self.player2.sprite.points = 0
			if self.player2.sprite.jump in self.player2.sprite.jumps:
				self.player2.sprite.jump += 1
		return state, state2
