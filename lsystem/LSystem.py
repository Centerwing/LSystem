from turtle.Turtle import *
from Conf import Conf
import pygame

from OpenGL.GL import *


class LSystem(object):
    """abstract class"""

    def __init__(self, turtle):
        self.turtle = turtle                    # 画图器
        self.LSName = "Undefined"               # 图形名称
        self.LSRules = {}                       # 产生式
        self.LSVars = {}                        # 与turtle的方法对应
        self.LSParams = {}                      # 变换参数
        self.LSAngle = math.pi / 2              # 默认旋转角度
        self.LSSegment = 1.0                    # 默认移动距离
        self.LSSteps = 5                        # 默认迭代次数
        self.LSStartingString = "F"             # 默认开始符
        self.LSStochastic = False               # 随机生成
        self.LSStochRange = 0.01                # 随机范围
        self.LSCode = ""                        # 当前字符串
        self.LSCodeLen = 0                      # 当前字符串长度

        self.LSVertexShader = ""
        self.LSPixelShader = ""

        self.LSDrawType = GL_LINE_STRIP         # 绘制连续直线

        self.defineParams()                     # 设置变换参数
        self.createVars()                       # 设置字符变换对应
        self.createRules()                      # 设置产生式

        self.currentMaxStep = 0                 # 最大迭代次数
        self.currentStep = 0                    # 当前迭代次数
        self.autorun = True                     # 控制自动迭代
        self.stepbystep = False                 # 步进
        self.createShaders()                    # 创建着色器
        self.compileShaders()                   # 编译着色器

        """ 以下变量需要在子类定义
                - LSName
                - LSAngle
                - LSSegment
                - LSStartingString
                - LSRules
                - LSParams
                - LSVars
         """

    def defineParams(self):
        raise NotImplementedError(
            "The method `defineParams' of the LSystem `" + self.LSName + "' has not been implemented yet")

    def createVars(self):
        raise NotImplementedError(
            "The method `createVars' of the LSystem `" + self.LSName + "' has not been implemented yet")

    def createRules(self):
        raise NotImplementedError(
            "The method `createRules' of the LSystem `" + self.LSName + "' has not been implemented yet")

    def createShaders(self):
        self.LSVertexShader = """
		in vec4 gl_Vertex;
		in vec4 gl_Color;
		uniform float time; // exemple of giving a uniform value
		varying vec4 vertex_color;
		void main() {
			gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
			vertex_color = gl_Color;
		}
	    """
        self.LSPixelShader = """
		varying vec4 vertex_color;
		void main() {
		    gl_FragColor = vertex_color;
		}
	    """
        self.LSUniforms = {
            'time': lambda: time.time()
        }

    def compileShaders(self):
        if not 'vec3 rgb2hsv(vec3 c)' in self.LSVertexShader:
            self.LSVertexShader = """
		vec3 rgb2hsv(vec3 c)
		{
		    vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
		    vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
		    vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));

		    float d = q.x - min(q.w, q.y);
		    float e = 1.0e-10;
		    return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
		}

		vec3 hsv2rgb(vec3 c)
		{
		    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
		    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
		    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
		}
""" + self.LSVertexShader

            vs = glCreateShader(GL_VERTEX_SHADER)
            fs = glCreateShader(GL_FRAGMENT_SHADER)

            glShaderSource(vs, self.LSVertexShader)
            glShaderSource(fs, self.LSPixelShader)

            glCompileShader(vs)

            glCompileShader(fs)

            self.shader = glCreateProgram()

            glAttachShader(self.shader, vs)
            glAttachShader(self.shader, fs)

            glLinkProgram(self.shader)

    def getShader(self):
        return self.shader

    def getUniforms(self):
        return self.LSUniforms

    def setSteps(self, n):
        if n < 1:
            self.LSSteps += n
        if self.LSSteps < 1:
            self.LSSteps = 1
        if n >= 1:
            self.LSSteps = n

    def generate(self):
        print("============= Fractal Name: ", self.LSName)

        self.LSCode = self.LSStartingString

        self.generate_param_rec(self.LSSteps)

        if self.LSStochastic:
            self.turtle.setStochasticFactor(self.LSStochRange)

        self.LSCodeLen = len(self.LSCode)

    def runTurtleRun(self, stepbystep=False):
        self.stepbystep = stepbystep

        self.turtle.setDrawType(self.LSDrawType)

        # initialize step by step engine
        if self.stepbystep:
            self.currentStep = 0
            self.currentMaxStep = 0
            self.inc_max_step()

        # Begin the command sequence
        self.turtle.begin()
        if self.stepbystep:
            while self.currentStep < self.currentMaxStep:
                tmp = [self.currentStep]
                self.execute(tmp)
                self.currentStep = tmp[0]
        else:
            count = [0]
            while count[0] < self.LSCodeLen:
                self.execute(count)
        self.turtle.end()

    def execute(self, pos):
        dbg = pos[0]
        char = self.LSCode[pos[0]]
        if pos[0] + 1 < self.LSCodeLen and self.LSCode[pos[0] + 1] == '(':
            arg = self.find_arg(pos)  # extract arguments of the instruction
            if arg is None:
                print("Error: no argument found '" + char + "' in: ", self.LSCode[dbg:dbg + 10])
                return

            for param in self.LSParams:
                if param in arg:
                    arg = arg.replace(param, str(float(self.LSParams[param])))
            res = eval(arg)  # calculate param

            if char in self.LSVars:
                self.LSVars[char](res)  # call corresponding function
        else:
            if char in self.LSVars:
                self.LSVars[char](self.LSParams[char])  # call corresponding function
            pos[0] += 1

    def event(self, e):
        if e.type == pygame.KEYDOWN and self.currentMaxStep < self.LSCodeLen:
            if e.unicode == 'n':
                self.inc_max_step()
            if e.unicode == 'r':
                self.autorun = not self.autorun
            if e.unicode == '+':
                Conf.LSYSTEM.AUTORUN_STEP *= 10
            if e.unicode == '-':
                Conf.LSYSTEM.AUTORUN_STEP /= 10

    """ used for step by step """
    def update(self):
        if self.stepbystep:
            self.turtle.begin()
            if self.autorun:
                self.inc_max_step(step=Conf.LSYSTEM.AUTORUN_STEP)
            while self.currentStep < self.currentMaxStep:
                tmp = [self.currentStep]
                self.execute(tmp)
                self.currentStep = tmp[0]
            self.turtle.end()

    # recursively generate
    def generate_param_rec(self, itern):
        self.LSCodeLen = len(self.LSCode)
        if itern == 0:
            return

        rplc_list = []
        la = [0]  # look ahead

        while la[0] < self.LSCodeLen:
            rplc_list.append(self.apply_rule(la))

        newcode = ''.join(rplc_list)

        self.LSCode = newcode

        self.generate_param_rec(itern - 1)

    def apply_rule(self, la):
        char = self.LSCode[la[0]]  # get current character
        r = self.rules_contain(char)  # get the corresponding rule

        if r is not False:
            arg = self.find_arg(la)

            if not arg:
                return self.LSRules[r]

            param = self.find_param(r)
            parametized_rule = self.LSRules[r].replace(param, arg)  # replace the param name by its value

            return parametized_rule

        else:
            la[0] += 1
            return char

    """ find param name in a bracket """
    def find_param(self, r):
        s = 0
        t = 0
        for k in range(len(r)):
            if r[k] == '(':
                s = k
            if r[k] == ')':
                t = k
        if t is 0 or s is t:
            return None
        return r[s + 1:t]

    """ find param name in a bracket """
    def find_arg(self, la):
        la[0] += 1
        if la[0] >= self.LSCodeLen:
            return None
        if self.LSCode[la[0]] != '(':
            return None
        k = la[0]
        while self.LSCode[k] != ')':
            k += 1  # find the closing bracket
        res = self.LSCode[la[0] + 1:k]
        la[0] = k + 1
        return res

    def rules_contain(self, char):
        for r in self.LSRules:
            if r[0] == char:
                return r
        return False

    def inc_max_step(self, step=1):
        if self.currentMaxStep < self.LSCodeLen:
            self.currentMaxStep += step
            while self.currentMaxStep < self.LSCodeLen and self.LSCode[self.currentMaxStep] not in self.LSVars:
                self.currentMaxStep += 1
        if self.currentMaxStep >= self.LSCodeLen:
            self.currentMaxStep = self.LSCodeLen - 1
