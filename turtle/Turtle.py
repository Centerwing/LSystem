from Vector import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import pdb
import math
import colorsys

from Conf import Conf
import random
import numpy as np
import time


# 绘制图像的类，提供了基本操作
class Turtle:
    # 保存状态的类，用于绘制分支
    class State:

        def __init__(self, pos, heading, color):
            self.pos = Vector().set(pos)
            self.heading = Vector().set(heading)
            self.color = Vector().set(color)

    def __init__(self, pos=None):
        # 初始化当前位置，朝向，颜色
        if pos is None:
            self.pos = Vector(Conf.TURTLE.INIT_POS)
        else:
            self.pos = Vector(pos)
        self.heading = Vector(Conf.TURTLE.INIT_HEADING)
        self.color = Vector(
            colorsys.rgb_to_hls(Conf.TURTLE.INIT_COLOR[0], Conf.TURTLE.INIT_COLOR[1], Conf.TURTLE.INIT_COLOR[2]))

        self.stateStack = []  # 保存状态的栈，用于绘制分支
        self.stochasticFactor = 0  # 随机因子

        # 保存要绘制的所有点
        self.vertexBuffer = []
        self.vertexBufferLength = 0
        self.vertexBufferChanged = False
        self.vertexPositions = None
        self.draw_type = GL_TRIANGLES

        self.point()

    # 设置openGL的绘制类型
    def setDrawType(self, type):
        self.draw_type = type

    # 设置随机因子
    def setStochasticFactor(self, factor):
        self.stochasticFactor = factor

    # 变量会在(1-factor)*value到(1+factor)*value间随机
    def randomize(self, value):
        if self.stochasticFactor:
            return ((random.random() * 2 * self.stochasticFactor) - self.stochasticFactor) * value + value
        return value

    # 重新初始化
    def reinit(self):
        self.pos = Vector(Conf.TURTLE.INIT_POS)
        self.heading = Vector(Conf.TURTLE.INIT_HEADING)
        self.color = Vector(
            colorsys.rgb_to_hls(Conf.TURTLE.INIT_COLOR[0], Conf.TURTLE.INIT_COLOR[1], Conf.TURTLE.INIT_COLOR[2]))

        self.vertexBuffer = []
        self.vertexBufferChanged = False
        self.vertexBufferLength = 0
        self.vertexPositions = vbo.VBO(np.array(self.vertexBuffer, dtype=np.float32))
        self.vertexPositions.bind()

    # 将当前点加入到要绘制的点集中，breakline代表分支的结束
    def point(self, breakline=0):
        c = colorsys.hls_to_rgb(self.color.x, self.color.y, self.color.z)
        self.vertexBuffer.append([float(self.pos.x), float(self.pos.y), float(self.pos.z),
                                  c[0], c[1], c[2], breakline])
        self.vertexBufferChanged = True
        self.vertexBufferLength += 1

    # 开始绘制的标志
    def begin(self, reinit=False):
        self.vertexBufferChanged = False

        if reinit:
            self.reinit()
            glutSolidSphere(0.1, 10, 10)

    # 将当前状态入栈
    def push(self, arg):
        self.stateStack.append(Turtle.State(self.pos, self.heading, self.color))

    # 将栈顶状态弹出并应用
    def pop(self, arg):
        state = self.stateStack.pop()
        self.pos.set(state.pos)
        self.heading.set(state.heading)
        self.color.set(state.color)
        self.point(1)

    # 向前移动step
    def forward(self, step):
        self.pos += self.randomize(step) * self.heading
        self.point()

    # 向后移动step
    def backward(self, step):
        if 'turtle' in Conf.DEBUG:
            print("Called: backward(", step, ");")
        self.pos += ((self.randomize(step) * self.heading) * -1)
        self.point()

    # 绕x轴逆时针旋转
    def rotX(self, angle):
        angle = self.randomize(angle)
        self.heading.set((
            self.heading.x,
            self.heading.y * math.cos(angle) - self.heading.z * math.sin(angle),
            self.heading.y * math.sin(angle) + self.heading.z * math.cos(angle)))

    # 绕x轴逆时针旋转
    def irotX(self, angle):
        angle = self.randomize(angle)
        angle = -angle
        self.heading.set((
            self.heading.x,
            self.heading.y * math.cos(angle) - self.heading.z * math.sin(angle),
            self.heading.y * math.sin(angle) + self.heading.z * math.cos(angle)))

    def rotY(self, angle):
        angle = self.randomize(angle)
        self.heading.set((
            self.heading.x * math.cos(angle) + self.heading.z * math.sin(angle),
            self.heading.y,
            - self.heading.x * math.sin(angle) + self.heading.z * math.cos(angle)))

    def irotY(self, angle):
        angle = self.randomize(angle)
        angle = -angle
        self.heading.set((
            self.heading.x * math.cos(angle) + self.heading.z * math.sin(angle),
            self.heading.y,
            - self.heading.x * math.sin(angle) + self.heading.z * math.cos(angle)))

    def rotZ(self, angle):
        angle = self.randomize(angle)
        self.heading.set((
            self.heading.x * math.cos(angle) - self.heading.y * math.sin(angle),
            self.heading.x * math.sin(angle) + self.heading.y * math.cos(angle),
            self.heading.z))

    def irotZ(self, angle):
        angle = self.randomize(angle)
        angle = -angle
        self.heading.set((
            self.heading.x * math.cos(angle) - self.heading.y * math.sin(angle),
            self.heading.x * math.sin(angle) + self.heading.y * math.cos(angle),
            self.heading.z))

    # 设置颜色
    def setColor(self, color):
        self.color.set(colorsys.rgb_to_hls(color[0], color[1], color[2]))

    # 下一个颜色，用于产生颜色渐变效果
    def nextColor(self, step):
        self.color.x += step
        if self.color.x > 1.0:
            self.color.x = self.color.x - 1.0

    def end(self):
        pass

    # 创建vbo，并将点全部绘制
    def draw(self):
        if self.vertexBufferChanged or self.vertexPositions is None:
            vertices = np.array(self.vertexBuffer,
                                dtype=np.float32)
            self.vertexPositions = vbo.VBO(vertices)
            # print("Total number of vertex: ", self.vertexBufferLength)
            self.vertexBufferChanged = False

        self.vertexPositions.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        glVertexPointer(3, GL_FLOAT, 28, self.vertexPositions)  # 三个位置坐标
        glColorPointer(3, GL_FLOAT, 28, self.vertexPositions + 12)  # 三个颜色值
        # glVertexAttribPointer(7, 1, GL_FLOAT, GL_TRUE, 28, self.vertexPositions+24)

        glDrawArrays(self.draw_type, 0, self.vertexBufferLength)

        self.vertexPositions.unbind()
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
