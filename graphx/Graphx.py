import pygame
from pygame.locals import *

from OpenGL.arrays import vbo

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from graphx.Camera import Camera
from Conf import Conf

import numpy as np


class Graphx:

    def __init__(self):

        self.width, self.height = 1280, 800
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), OPENGL | DOUBLEBUF)

        glMatrixMode(GL_PROJECTION)  # 设置投影矩阵
        glLoadIdentity()
        gluPerspective(65.0, self.width / float(self.height), 0.01, 1000.0)  # 透视投影，参数为角度，宽高比，远近裁剪平面距离
        glMatrixMode(GL_MODELVIEW)  # 设置模型矩阵
        glEnable(GL_DEPTH_TEST)  # 开启深度测试，实现遮挡关系
        self.camera = Camera((0.0, 0, 0))

        # 底部黑色平面
        vertices = np.array(  # 创建顶点数据集
            [[100.0, -10.0, 100.0, Conf.GRAPHX.BASE_COLOR[0], Conf.GRAPHX.BASE_COLOR[1], Conf.GRAPHX.BASE_COLOR[2]],
             [-100.0, -10.0, 100.0, Conf.GRAPHX.BASE_COLOR[0], Conf.GRAPHX.BASE_COLOR[1], Conf.GRAPHX.BASE_COLOR[2]],
             [-100.0, -10.0, -100.0, Conf.GRAPHX.BASE_COLOR[0], Conf.GRAPHX.BASE_COLOR[1], Conf.GRAPHX.BASE_COLOR[2]],
             [100.0, -10.0, -100.0, Conf.GRAPHX.BASE_COLOR[0], Conf.GRAPHX.BASE_COLOR[1], Conf.GRAPHX.BASE_COLOR[2]]],
            dtype=np.float32)
        self.vertexPositions = vbo.VBO(vertices)
        # 创建index
        indices = np.array([[0, 1, 2], [0, 3, 2]], dtype=np.int32)  # 顶点数据集的索引
        self.indexPositions = vbo.VBO(indices, target=GL_ELEMENT_ARRAY_BUFFER)
        self.uniform_values = {}
        self.uniform_locations = {}  # 统一变量

    # 指定着色器：glAttachShader()->glCompileShader()->glLinkProgram()->glUseProgram()
    def setShader(self, shader, unif):
        glUseProgram(shader)
        self.shader = shader
        self.uniform_values = unif
        for name in unif:
            self.uniform_locations[name] = glGetUniformLocation(self.shader, name)

    # 绘制黑色的平面   和坐标系
    def draw_base(self):

        self.indexPositions.bind()
        self.vertexPositions.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        glVertexPointer(3, GL_FLOAT, 24, self.vertexPositions)  # 绘制前指定顶点数组，参数是顶点坐标数，数据类型，顶点偏移(顶点字节数)
        glColorPointer(3, GL_FLOAT, 24, self.vertexPositions + 12)

        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        self.indexPositions.unbind()
        self.vertexPositions.unbind()
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)

        # 坐标系
        """
        glBegin(GL_LINES)
        glColor3f(1, 0, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(100, 0, 0)
        glColor3f(0, 1, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 100, 0)
        glColor3f(0, 0, 1)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 100)
        glEnd()
        """

    @staticmethod
    def clear():  # 每次绘制前要清除缓冲区
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # 绘制背景，底部，更新视点并展示
    def update(self, lookat=(0, 0, 0)):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.camera.look(lookat)

        for name in self.uniform_values:
            # print "setting ", name, ":", self.uniform_locations[name], "=", self.uniform_values[name]()
            glUniform1f(self.uniform_locations[name], self.uniform_values[name]())

        # self.draw_base()

        glClearColor(1, 1, 1, 1)
        pygame.display.flip()

    def event(self, e):
        self.camera.event(e)
