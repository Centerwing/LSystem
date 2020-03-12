from lsystem.LSystem import LSystem
import math


class Snowflake(LSystem):
	def defineParams(self):
		self.LSName = "Snowflake"
		self.LSAngle = math.pi / 3
		self.LSSegment = 0.01
		self.LSSteps = 8
		self.LSStartingString = "F++F++F"

	def createVars(self):
		self.LSVars = {
			'F':	self.turtle.forward,
			'+':	self.turtle.rotZ,
			'-':	self.turtle.irotZ
		}
		self.LSParams = {
			'F':	self.LSSegment,
			'+':	self.LSAngle,
			'-':	self.LSAngle
		}

	def createRules(self):
		self.LSRules = {
			'F':	"F-F++F-F"
		}
