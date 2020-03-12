import math
import pygame.locals

from graphx.Graphx import *
from turtle.Turtle import *
from lsystem import *

USED = [
	lambda t: Tree1.Tree1(t),
	lambda t: Tree1.Tree1(t, -math.pi / 32),
	lambda t: Tree1.Tree1(t, -math.pi / 64),
	lambda t: Tree3.Tree3(t),
	lambda t: Tree3.Tree3(t, 0.2, 0),
	lambda t: Tree3.Tree3(t, -0.2, 0),
	lambda t: Tree3.Tree3(t, 0, -math.pi / 16),
	lambda t: Tree3.Tree3(t, 0.1, -math.pi / 16),
	lambda t: Tree3.Tree3(t, -0.1, -math.pi / 16),
	lambda t: Tree3.Tree3(t, 0, math.pi / 8),
	lambda t: Tree4.Tree4(t, 1, 0),
	lambda t: Tree4.Tree4(t, 5, 0),
	lambda t: Tree4.Tree4(t, 3, 0),
]


class Main:
	def __init__(self):
		self.gx = Graphx()

		self.quit = False

		self.fractals = []
		self.turtles = []

		self.grid_length = 30
		self.fractal_size = -1
		self.random_factor = 15
		self.debug = False

		self.parse_input()

		self.init_grid(self.grid_length, self.random_factor)

	def parse_input(self):
		for arg in sys.argv:
			if ".py" in arg:
				continue
			if arg == "debug":
				self.debug = True
			tmp = arg.split("=")
			if tmp[0] == "length":
				self.grid_length = int(tmp[1])
			if tmp[0] == "debug":
				self.debug = True
				if len(tmp) > 1:
					if tmp[1] != "True":
						self.debug = False

	def init_grid(self, length, rand_factor):
		for x in range(length):
			for y in range(length):
				randx = random.random() * rand_factor
				posx = -2.5*length + x * length * 5 / (length - 1) + randx
				randy = random.random() * rand_factor
				posy = -2.5*length + y * length * 5 / (length - 1) + randy
				print(posx, ' and  ', posy)
				t = Turtle((posx, 0, posy))
				self.turtles.append(t)
				self.fractals.append(USED[random.randint(0, len(USED) - 1)](t))

	def event(self, e):
		if e.type == pygame.QUIT:
			self.quit = True
		for f in range(len(self.fractals)):
			self.fractals[f].event(e)
		self.gx.event(e)

	def main(self):
		print("=============== Starting world generation, please wait... ===============")

		for f in range(len(self.fractals)):
			self.fractals[f].setSteps(self.fractal_size)
			self.fractals[f].generate()

		for f in range(len(self.fractals)):
			self.fractals[f].runTurtleRun(stepbystep=('debug' in sys.argv))
		print("=============== World generation successfully done ! ===================")

		while not self.quit:
			for e in pygame.event.get():
				self.event(e)
			self.gx.clear()
			for f in range(len(self.fractals)):
				self.fractals[f].update()
				self.gx.setShader(self.fractals[f].getShader(), self.fractals[f].getUniforms())
				self.turtles[f].draw()
			self.gx.update()


Main().main()
