import pygame, sys
from settings import *
from world import World
from pool import pool
import pandas as pd
import os
import time
import pygame_textinput
pygame.init()
#screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")
ranges = [[i, i + 150] for i in range(50, 3350, 150)]
BLACK = (0, 0, 0)
YELLOW = (220, 200, 0)
WHITE = (255, 255, 255)
#print(ranges)
class Platformer:
	def __init__(self, subject_name):
		self.level = 0
		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.clock = pygame.time.Clock()
		self.WIDTH, self.HEIGHT = pygame.display.get_surface().get_size()
		self.player_event = False
		self.images = os.listdir('assets/terrain/background')
		self.bg_img = pygame.image.load('assets/terrain/background/1.jpg')
		self.bg_img = pygame.transform.scale(self.bg_img, (self.WIDTH, self.HEIGHT))
		self.state = None
		self.points = 0
		self.glevel = -2
		self.gjump = 0
		self.pygame_rect = pygame.Rect(1770, 0, 150, 150)
		self.dcts = []
		self.subject_name = subject_name
		#self.pygame_rect = pygame.Rect(500, 0, 150, 150)

	def respwan(self, player):
		#print(self.world.player.sprite.rect.x)
		#print(self.world.player.sprite.rect.x)
		for range in ranges:
			if range[0] <= player.sprite.rect.x < range[1]:
				player.sprite.rect.x = range[0]
		player.sprite.rect.y = 300
	def respawn2(self, player):
		player.sprite.rect.x = player.start[0]
		player.sprite.rect.y = player.start[1]

	def update_screen(self):
		self.WIDTH, self.HEIGHT = pygame.display.get_surface().get_size()
		self.bg_img = pygame.transform.scale(self.bg_img, (self.WIDTH, self.HEIGHT))
		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	def main(self, timer):
		tim = timer
		pygame.display.set_caption("Platformer")
		self.update_screen()
		self.world = World(world_map[self.glevel], self.screen, self.WIDTH, self.HEIGHT)
		self.world.player2.sprite.points = self.points
		self.world.player2.sprite.jump = self.gjump
		self.world.player2.sprite.level = self.glevel
		self.bg_img = pygame.image.load('assets/terrain/background/' + self.images[self.glevel])
		self.bg_img = pygame.transform.scale(self.bg_img, (self.WIDTH, self.HEIGHT))
		self.ai_event = None
		while True:
			#print(self.world.player1.sprite.rect.y)
			self.screen.blit(self.bg_img, (0, 0))
			self.ai_event = None
			if self.glevel > -1:
				if abs(self.world.player1.sprite.rect.x + 5) < self.world.player2.sprite.rect.x:
					self.ai_event = 'space'
				if self.world.player1.sprite.rect.y <= 450 and self.ai_event == 'space':
					self.ai_event = 'right'
				if abs(self.world.player1.sprite.rect.x + 5) >= self.world.player2.sprite.rect.x:
					self.ai_event = None
				if abs(self.world.player1.sprite.rect.x + 5) > self.world.player2.sprite.rect.x:
					self.ai_event = 'space'
				if self.world.player1.sprite.rect.y <= 450 and self.ai_event == 'space':
					self.ai_event = 'left'
				if self.world.player1.sprite.rect.x == self.world.player2.sprite.rect.x:
					self.ai_event = None
				if self.world.player2.sprite.jump_fail():
					self.ai_event = 'right'
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						self.player_event = "left"
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						sys.exit()
					if event.key == pygame.K_RIGHT:
						self.player_event = "right"
					if event.key == pygame.K_UP:
						self.world.player2.sprite.jump += 1
						self.player_event = "space"
					if event.key == pygame.K_2:
						self.glevel = 0
						self.gjump = 0
						self.points = 0
						self.world.player2.sprite.jump = 0
						play.dcts.append(pool('start'))
						df = pd.DataFrame(self.dcts)
						df.to_excel(f'{self.subject_name}.xlsx')
						tim = time.process_time()
						return 'restart', tim
					if event.key == pygame.K_1:
						self.glevel = -2
						return 'restart', tim
				elif event.type == pygame.KEYUP:
					self.player_event = False

			state, state2 = self.world.update(player_event=self.player_event, ai_event=self.ai_event, timer=tim, level=self.glevel)
			if self.world.player2.sprite.jump > 305:
				self.world.game.game_over()
				self.dcts.append(pool('end'))
				df = pd.DataFrame(self.dcts)
				df.to_excel(f'{self.subject_name}.xlsx')
				return 'end', tim
			if state == 'respawn' or state2 == 'respawn' or state == 'next' or state == 'restart':
				break
			if state2 == 'respawn':
				self.respawn2(self.world.player1)
			pygame.draw.rect(self.screen, 'black', self.pygame_rect)
			pygame.display.update()
			self.clock.tick(60)
		if state == 'next':
			if self.glevel < 0:
				self.glevel += 1
				if self.glevel == 0:
					self.glevel = -2
			elif self.glevel > -1:
				self.glevel = (self.glevel + 1) % 6

			self.gjump = self.world.player2.sprite.jump
			self.points = self.world.player2.sprite.points
			self.level %= 6
			return 'restart', tim
		if state == 'restart' or state == 'respawn' or state2 == 'respawn':
			self.points = 0
			if self.glevel < 0:
				self.glevel = -2
			else:
				self.glevel = 0
			self.gjump = self.world.player2.sprite.jump
			if self.glevel > -1:
				if state == 'respawn':
					self.dcts.append(pool('player',jump=self.gjump))
					df = pd.DataFrame(self.dcts)
					df.to_excel(f'{self.subject_name}.xlsx')
				if state2 == 'respawn' and state != 'respawn':
					self.dcts.append(pool('ai',jump=self.gjump - 1))
					df = pd.DataFrame(self.dcts)
					df.to_excel(f'{self.subject_name}.xlsx')
			return 'restart', tim


if __name__ == "__main__":

	textinput = pygame_textinput.TextInputVisualizer()

	screen = pygame.display.set_mode((1000, 200))
	pygame.display.set_caption("Enter Subject name")
	clock = pygame.time.Clock()
	running = True
	while running:
		screen.fill((225, 225, 225))

		events = pygame.event.get()

		# Feed it with events every frame
		textinput.update(events)
		# Blit its surface onto the screen
		screen.blit(textinput.surface, (10, 10))

		for event in events:
			if event.type == pygame.QUIT:
				running = False

		pygame.display.update()
		clock.tick(30)
	subject_name = textinput.value
	play = Platformer(subject_name=subject_name)
	t = time.process_time()
	while True:
		state, t = play.main(timer=t)
		if state == 'restart':
			continue
		else:
			break
