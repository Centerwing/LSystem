from lsystem.LSystem import LSystem
import math

class Tree3(LSystem):
	def __init__(self, turtle, modif_seg=0, modif_angle=0):
		self.modif_seg = modif_seg
		self.modif_angle = modif_angle
		super(Tree3, self).__init__(turtle)

	def defineParams(self):
		self.LSName = "Tree 3"
		self.LSAngle = math.pi / 8 + self.modif_angle
		self.LSSegment = 1 + self.modif_seg
		self.LSSteps = 4
		self.LSStartingString = "F"
		self.LSStochastic = True
		self.LSStochRange = 1

	def createVars(self):
		self.LSVars = {
			'F':	self.turtle.forward,
			'+':	self.turtle.rotZ,
			'-':	self.turtle.irotZ,
			'<':	self.turtle.rotX,
			'>':	self.turtle.irotX,
			'[':	self.turtle.push,
			']':	self.turtle.pop,
			'I':	self.turtle.setColor,
			'Y':	self.turtle.setColor
		}
		self.LSParams = {
			'F':	self.LSSegment,
			'+':	self.LSAngle,
			'-':	self.LSAngle,
			'<':	self.LSAngle,
			'>':	self.LSAngle,
			'[':	None,
			']':	None,
			'I':	(0.5, 0.25, 0),
			'Y':	(0, 0.5, 0)
		}

	def createRules(self):
		self.LSRules = {
			'F':	"IFF[Y-FF][Y+FF][Y<FF][Y>FF]"
		}
