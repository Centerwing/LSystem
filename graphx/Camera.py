import math
import time

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame

from Conf import Conf
from Vector import *


class Camera:

    def __init__(self, look):
        # 更新视点时，镜头每次转动角度
        self.angleY = 0
        self.angleX = 0
        self.angleZ = 0
        self.posX = 0
        self.posY = 0
        self.posZ = 0
        # 相机距离物体的距离，xyz坐标一致
        self.distance = 100
        # 设定视点
        gluLookAt(0.0, 0.0, 0.0,  # 相机位置
                  look[0], look[1], look[2],  # 看向的东西的位置
                  0.0, 1.0, 0.0)  # 相机的头的朝向(不是镜头的朝向)
        # 记录看向的位置和时间，每秒更新一次视点
        self.lookat = (0.0, 0.0, 0.0, time.time())
        # 设置按键延迟，第一次响应为500ms，后续每隔10ms响应一次
        pygame.key.set_repeat(10, 10)

    def update(self):  # 镜头自动转动，改变角度
        self.angleY -= Conf.GRAPHX.CAMERA_ROTATION_VELOC
        pass

    # 处理按键
    def event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.unicode == 'd':
                self.angleZ += 1
            if e.unicode == 'a':
                self.angleZ -= 1
            if e.unicode == 'w':
                self.angleX += 1
            if e.unicode == 's':
                self.angleX -= 1
            if e.unicode == 'q':
                self.angleY += 1
            if e.unicode == 'e':
                self.angleY -= 1
            if e.key == pygame.K_RETURN:
                self.angleX = 0
                self.angleZ = 0
                self.distance = 100
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 5:
                self.distance *= 1.1
            if e.button == 4:
                self.distance *= 0.9
        pass

    def look(self, lookat):  # 每隔一段时间更新视点
        # 更新时间
        if time.time() - self.lookat[3] > Conf.GRAPHX.CAMERA_UPDATE_PERIOD or lookat is (0, 0, 0):
            self.lookat = (lookat[0], lookat[1], lookat[2], time.time())
        gluLookAt(self.lookat[0] + self.distance, self.lookat[1] + self.distance, self.lookat[2] + self.distance,
                  self.lookat[0], self.lookat[1], self.lookat[2],
                  0, 1, 0)
        glRotated(self.angleY, 0, 1, 0)
        glRotated(self.angleX, 1, 0, 0)
        glRotated(self.angleZ, 0, 0, 1)
