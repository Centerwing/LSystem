from lsystem.LSystem import LSystem
import math


class Tree2D(LSystem):
	def defineParams(self):
		self.LSName = "Tree2D"
		self.LSAngle = math.pi / 6
		self.LSSegment = 0.01
		self.LSSteps = 5
		self.LSStartingString = "F"

	def createVars(self):
		self.LSVars = {
			'F':	self.turtle.forward,
			'+':	self.turtle.rotZ,
			'-':	self.turtle.irotZ,
			'[':	self.turtle.push,
			']':	self.turtle.pop

		}
		self.LSParams = {
			'F':	self.LSSegment,
			'+':	self.LSAngle,
			'-':	self.LSAngle,
			'[':	None,
			']':	None
		}

	def createRules(self):
		self.LSRules = {
			'F':	"FF[--F][-F][+F][++F]"
		}
