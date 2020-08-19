#!/usr/bin/env python3

import pygame
import random
import time


class Snake:
	def __init__(self):
		self.len = 1
		self.s = SQUARE_SIZE
		body = v2()
		body.x, body.y = LEVELS[LEVEL].start.x, LEVELS[LEVEL].start.y
		self.body = [body]
		self.speed = v2()
		self.speed.x, self.speed.y = 1, 0
		self.pos = v2()
		self.pos.x, self.pos.y = self.body[0].x, self.body[0].y

	def show(self, surf):
		for p in self.body:
			pygame.draw.rect(surf, GREEN, (int(p.x * self.s), int(p.y * self.s), self.s, self.s))

	def move(self):
		old = v2()
		old.x, old.y = self.body[0].x, self.body[0].y
		self.body[0].x += self.speed.x
		self.body[0].y += self.speed.y
		if self.body[0].x == -1:
			self.body[0].x = int(SCREENWIDTH / self.s)
		elif self.body[0].x == int(SCREENWIDTH / self.s):
			self.body[0].x = 0
		elif self.body[0].y == -1:
			self.body[0].y = int(SCREENHEIGHT / self.s)
		elif self.body[0].y == int(SCREENHEIGHT / self.s):
			self.body[0].y = 0
		for p in range(1, self.len):
			self.body[p], old = old, self.body[p]

		self.pos.x, self.pos.y = self.body[0].x, self.body[0].y

	def crash(self):
		crashed = self.body[0] in self.body[1:] or self.body[0] in LEVELS[LEVEL].walls
		return crashed

	def eat(self, foo):
		if self.pos == foo.pos:
			global SCORE, LEVEL
			self.len += 1
			new = v2()
			new.x, new.y = self.body[0].x - self.speed.x, self.body[0].y - self.speed.y
			self.body.append(new)
			foo = Food()
			SCORE += 1
		return foo


class Food:
	def __init__(self):
		self.s = SQUARE_SIZE
		self.pos = v2()
		self.pos.x, self.pos.y = random.randrange(0, GRID - 1), random.randrange(0, int(SCREENHEIGHT / self.s) - 1)
		while self.pos in LEVELS[LEVEL].walls:
			self.pos.x, self.pos.y = random.randrange(0, GRID - 1), random.randrange(0, int(SCREENHEIGHT / self.s) - 1)

	def show(self, surf):
		pygame.draw.rect(surf, RED, (int(self.pos.x) * self.s, int(self.pos.y) * self.s, self.s, self.s))


class Level:
	def __init__(self, file):
		self.walls = []
		with open(file, 'r') as f:
			for y in range(40):
				for x, s in enumerate(f.readline()):
					if s == '1':
						self.walls.append(v2(x, y))
			self.start = v2(list(map(int, f.readline().split(',')))[::-1])
			self.max = int(f.readline())
		self.wall_size = SQUARE_SIZE

	def show(self, surf):
		for w in self.walls:
			pygame.draw.rect(surf, BLUE, (int(w.x * self.wall_size), int(w.y * self.wall_size), self.wall_size, self.wall_size))
		score = FONT.render(str(SCORE), False, RED)
		surf.blit(score, (0, 0))


def main():
	f = 0
	s = Snake()
	food = Food()
	running = True
	m = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN and s.speed.y != -1 and m:
					s.speed.x, s.speed.y = 0, 1
					m = False
				elif event.key == pygame.K_UP and s.speed.y != 1 and m:
					s.speed.x, s.speed.y = 0, -1
					m = False
				elif event.key == pygame.K_RIGHT and s.speed.x != -1 and m:
					s.speed.x, s.speed.y = 1, 0
					m = False
				elif event.key == pygame.K_LEFT and s.speed.x != 1 and m:
					s.speed.x, s.speed.y = -1, 0
					m = False
		f += 1
		global LEVEL, SCORE
		if f == 4:
			f = 0
			m = True
			s.move()
			if s.crash():
				f = 0
				s = Snake()
				food = Food()
				m = True
				SCORE = 0
		screen.fill(BLACK)
		food.show(screen)
		s.show(screen)
		food = s.eat(food)

		if SCORE > LEVELS[LEVEL].max:
			LEVEL += 1
			s = Snake()
			SCORE = 0
			screen.fill(BLACK)
			food.show(screen)
			s.show(screen)
			LEVELS[LEVEL].show(screen)
			pygame.display.update()
			time.sleep(1)

		LEVELS[LEVEL].show(screen)
		pygame.display.update()


if __name__ == '__main__':
	pygame.init()
	pygame.font.init()

	SCREENWIDTH = 720
	SCREENHEIGHT = 720

	GRID = 40
	SQUARE_SIZE = int(SCREENWIDTH / GRID)

	RED = (255, 0, 0)
	GREEN = (0, 255, 0)
	BLUE = (0, 0, 255)
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	FONT = pygame.font.SysFont('Andale Mono Regular', 50)

	v2 = pygame.math.Vector2

	screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
	pygame.display.set_caption('Snake')

	SCORE = 0

	LEVELS = []

	level0 = Level('levels/level0.sn')
	LEVELS.append(level0)

	level1 = Level('levels/level1.sn')
	LEVELS.append(level1)

	LEVEL = 0

	main()
	pygame.quit()
