# -*- coding:utf-8 -*-
import pygame
from math import sin, cos, pi

class Hexagon(pygame.sprite.Sprite):
    def __init__(self, posx=0, posy=0, id_and_pos=(0, 0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.points = []
        self.color = (50, 150, 50)
        self.activ = False
        self.id_and_pos = id_and_pos
        v = 0
        for i in range(6):
            self.points.append((cos(v)*((self.rect.width//2)-2)+self.rect.x, sin(v)*((self.rect.width//2)-2)+self.rect.y))
            v += (pi*2)/6

    def blit(self, surface, snake, prey):
        if self.id_and_pos in snake:
            pygame.draw.polygon(surface, (200, 50, 50), self.points, 0)
        elif self is prey:
            pygame.draw.polygon(surface, (50, 50, 200), self.points, 0)
        else:
            pygame.draw.polygon(surface, self.color, self.points, 0)
        pygame.draw.lines(surface, (50, 50, 200), 1, self.points, 2)