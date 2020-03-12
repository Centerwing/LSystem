import sys
import math
import time

from OpenGL.GLUT import *
from OpenGL.GL import *
import pygame
import pygame.locals

from graphx.Graphx import *
from turtle.Turtle import *
from lsystem import *
from Conf import Conf

# command line arguments
ARGUMENTS = {
	'tree1': 	lambda t: Tree1.Tree1(t),
	'tree2D':	lambda t: Tree2D.Tree2D(t),
	'tree3':	lambda t: Tree3.Tree3(t),
	'snow':	    lambda t: Snowflake.Snowflake(t),
	'hilbert':	lambda t: HilbertCurve.HilbertCurve(t),
	'koch':		lambda t: KochCurve.KochCurve(t),
	'levy':	    lambda t: LevyC.LevyC(t),
	'tree4':	lambda t: Tree4.Tree4(t),
	'default':	lambda t: HilbertCurve.HilbertCurve(t)
}


class Main:
	def __init__(self):
		self.turtle = Turtle()

		self.gx = Graphx()

		[self.fractal, steps] = self.parse_input()
		self.fractal.setSteps(steps)

		self.quit = False
		self.follow_building = False

	def event(self, e):
		if e.type == pygame.QUIT:
			self.quit = True
		elif e.type == pygame.KEYDOWN:
			if e.key == pygame.K_ESCAPE:
				self.quit = True
			elif e.key == pygame.K_SPACE:
				self.follow_building = not self.follow_building
		self.gx.event(e)
		if self.fractal is not None:
			self.fractal.event(e)

	# handle command line argument
	def parse_input(self):
		lsys = None
		lsstep = 0
		for arg in sys.argv:
			if arg == 'debug':
				print("Debug mode activated.")
				Conf.DEBUG['lsystem'] = 1
			if arg in ARGUMENTS:
				lsys = ARGUMENTS[arg](self.turtle)
			try:
				lsstep = int(arg)
			except Exception as e:
				continue
		if lsys is None:
			print("Error: Unkonwn or unspecified fractal name.")
			exit()
		return (lsys, lsstep)

	def main(self):
		self.fractal.generate()

		self.fractal.runTurtleRun(stepbystep=('lsystem' in Conf.DEBUG and Conf.DEBUG['lsystem'] >= 1))

		self.gx.setShader(self.fractal.getShader(), self.fractal.getUniforms())
		while not self.quit:
			for e in pygame.event.get():
				self.event(e)
			self.fractal.update()
			self.gx.clear()
			self.turtle.draw()
			if self.follow_building:
				self.gx.update(self.turtle.pos.toTuple())
			else:
				self.gx.update()


Main().main()
