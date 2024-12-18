import pygame
import time

pygame.font.init()

class Game:
	def __init__(self, screen, width, height):
		self.screen = screen
		self.font = pygame.font.Font("fonts/maturamtscriptcapitals.ttf",150)
		self.font1 = pygame.font.Font("fonts/maturamtscriptcapitals.ttf",75)
		self.font2 = pygame.font.Font("fonts/maturamtscriptcapitals.ttf",300)
		self.font3 = pygame.font.Font("fonts/maturamtscriptcapitals.ttf",300)
		self.font4 = pygame.font.SysFont('bloodcyrillic', 100)
		self.message_color = pygame.Color("darkorange")
		self.WIDTH, self.HEIGHT = width, height
		self.pygame_rect = pygame.Rect(1770, 0, 150, 150)
		#self.pygame_rect = pygame.Rect(500, 0, 150, 150)

	# if player2_2 ran out of life or fell below the platform
	def _game_lose(self, player):
		player.game_over = True
		message = self.font.render('- 10 points', True, self.message_color)
		self.screen.blit(message,(self.WIDTH // 3 + 70, 70))
		pygame.display.update()
		#pygame.time.delay(10000)
	def _game_respawn(self, player, player2):
		message = self.font2.render('Failed', True, 'crimson')
		#fail = self.font2.render('Failed!', True, 'crimson')
		#gover = self.font2.render('Game over', True, 'crimson')
		player2.points -= 10
		if player2.points < 0:
			player2.points = 0
		if player2.jump in player2.jumps:
			player2.jump += 1
		self.screen.fill('black')
		#self.screen.blit(gover, (self.WIDTH // 6, 100))
		#self.screen.blit(fail, (self.WIDTH // 6, 100))
		self.screen.blit(message, (self.WIDTH // 6, 350))
		if player2.jump - 1 not in player2.jumps:
			pygame.draw.rect(self.screen, 'white', self.pygame_rect)
			pygame.display.update()
			pygame.time.delay(1000)
			pygame.draw.rect(self.screen, 'black', self.pygame_rect)
			pygame.display.update()
			pygame.time.delay(1000)
			pygame.draw.rect(self.screen, 'white', self.pygame_rect)
			pygame.display.update()
			pygame.time.delay(1000)
			pygame.draw.rect(self.screen, 'black', self.pygame_rect)
			pygame.display.update()
			pygame.time.delay(7000)
		else:
			pygame.draw.rect(self.screen, 'white', self.pygame_rect)
			pygame.display.update()
			pygame.time.delay(1000)
			pygame.draw.rect(self.screen, 'black', self.pygame_rect)
			pygame.display.update()
			pygame.time.delay(9000)
	def game_over(self):
		self.screen.fill('black')
		message = self.font3.render('Game over!', True, 'crimson')
		self.screen.blit(message, (self.WIDTH // 8, 350))
		pygame.display.update()
		pygame.time.delay(10000)




	# if player2_2 reach the goal
	def _game_win(self, player):
		message = self.font.render('+ 50 points', True, self.message_color)
		player.points += 50
		self.screen.blit(message, (self.WIDTH // 4, 170))
		pygame.display.update()
		#pygame.time.delay(10000)
		#player2_2.game_over = True
		#player2_2.win = True
		#message = self.font.render('You Win!!', True, self.message_color)
		#self.screen.blit(message,(self.WIDTH // 3, 70))
		#player2_2.points += 50
		#pygame.time.delay(10000)

	def ai_state(self, player, player2, level=0):
		if player.rect.y >= self.HEIGHT - 30:
			if level > -1:
				self._game_respawn(player, player2)
			return 'respawn'
		else:
			return None

	# checks if the game is over or not, and if win or lose
	def game_state(self, player, player2, goal, level=0):
		if player2.rect.y >= self.HEIGHT:
			if level > -1:
				self._game_respawn(player, player2)
			return 'respawn'
		elif player2.rect.colliderect(goal.rect):
			return 'next'
		else:
			return None

	def show_life(self, player):
		life_size = 30
		img_path = "assets/life/life.png"
		life_image = pygame.image.load(img_path)
		life_image = pygame.transform.scale(life_image, (life_size, life_size))
		# life_rect = life_image.get_rect(topleft = pos)
		indent = 0
		for life in range(player.life):
			indent += life_size
			self.screen.blit(life_image, (indent, life_size))
	def show_score(self, player):
		#life_size = 15
		indent = 0
		#life_size = 15
		#img_path = "assets/life/life.png"
		#life_image = pygame.image.load(img_path)
		#life_image = pygame.transform.scale(life_image, (life_size, life_size))
		message = self.font1.render(f'Score: {player.points}', True, 'black')
		self.screen.blit(message, (500, 1))
		#pygame.display.update()
	def show_level(self, player):
		life_size = 30
		indent = 0
		life_size = 30
		img_path = "assets/life/life.png"
		life_image = pygame.image.load(img_path)
		life_image = pygame.transform.scale(life_image, (life_size, life_size))
		message = self.font.render(f'level: {player.level + 1}', True, self.message_color)
		self.screen.blit(message, (500, 1))
		#pygame.display.update()
	def show_jumps(self, player):
		life_size = 30
		indent = 0
		life_size = 30
		img_path = "assets/life/life.png"
		life_image = pygame.image.load(img_path)
		life_image = pygame.transform.scale(life_image, (life_size, life_size))
		message = self.font.render(f'jump: {player.jump}', True, self.message_color)
		self.screen.blit(message, (500, 1))
		#pygame.display.update()
	def show_online(self, player):
		#life_size = 15
		indent = 0
		#life_size = 15
		#img_path = "assets/life/life.png"
		#life_image = pygame.image.load(img_path)
		#life_image = pygame.transform.scale(life_image, (life_size, life_size))
		message = self.font1.render('Online', True, 'green')
		self.screen.blit(message, (1, 1))
		#pygame.display.update()
	def show_train(self, player):
		#life_size = 15
		indent = 0
		#life_size = 15
		#img_path = "assets/life/life.png"
		#life_image = pygame.image.load(img_path)
		#life_image = pygame.transform.scale(life_image, (life_size, life_size))
		message = self.font1.render('Training', True, 'green')
		self.screen.blit(message, (1, 1))
		#pygame.display.update()
	def show_offline(self, player):
		#life_size = 15
		indent = 0
		#life_size = 15
		#img_path = "assets/life/life.png"
		#life_image = pygame.image.load(img_path)
		#life_image = pygame.transform.scale(life_image, (life_size, life_size))
		message = self.font1.render('Offline', True, 'red')
		self.screen.blit(message, (1, 1))
		#pygame.display.update()
