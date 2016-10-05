# -*- coding:utf-8 -*-

import pygame, sys
from pygame.sprite import Sprite
from math import sin, cos, pi
from random import choice

SIZE = (640, 480)

window = pygame.display.set_mode(SIZE)
screen = pygame.Surface(SIZE)
finally_background = pygame.Surface(SIZE)
finally_background.set_alpha(0)

pygame.font.init()
ff = pygame.font.Font(None, 120)
ff2 = pygame.font.Font(None, 24)

class Hexagon(Sprite):
    def __init__(self, posx=0, posy=0, id_and_pos=(0, 0, 0)):
        Sprite.__init__(self)
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

hexes = []
posx = 0
posy = 0
x = 0
id = 0
for j in range(17):
    posx += 35
    y = 0
    for i in range(10):
        posy += 40
        hexes.append(Hexagon(posx=posx, posy=posy, id_and_pos=(id, x, y)))
        x += 2
        y += 1
    id += 1
    if posy == 400:
        posy = 20
        x = 1
    elif posy == 420:
        posy = 0
        x = 0

snake = [(8, 18, 9),
         (8, 16, 8),
         (8, 14, 7)]

vector = 1
id = 8
x = 14
y = 7
prey = 0
while 1:
    screen.fill((50, 50, 50))

    if not prey:
        prey = choice(hexes)
        while prey.id_and_pos in snake:
            prey = choice(hexes)

    if vector == 1:
        x -= 2
        y -= 1
    elif vector == 2:
        x -= 1
        if x % 2 != 0:
            y -= 1
        id += 1
    elif vector == 3:
        x += 1
        if x % 2 == 0:
            y += 1
        id += 1
    elif vector == 4:
        x += 2
        y += 1
    elif vector == 5:
        x += 1
        if x % 2 == 0:
            y += 1
        id -= 1
    elif vector == 6:
        x -= 1
        if x % 2 != 0:
            y -= 1
        id -= 1

    next_step = (id, x, y)
    if next_step not in snake:
        if prey.id_and_pos != next_step:
            snake.append(next_step)
            snake.pop(0)
        else:
            snake.append(next_step)
            prey = 0
            pygame.time.delay(10)
    else:
        vector = -1
    if id < 0 or id > 16 or y < 0 or y > 9:
        vector = -1

    for h in hexes:
        h.blit(screen, snake, prey)

    if vector == -1:
        alpha = finally_background.get_alpha()
        if alpha < 100:
            alpha += 1
            finally_background.set_alpha(alpha)
        screen.blit(finally_background, (0, 0))
        if len(snake) < 13:
            screen.blit(ff.render('Поражение!', 1, (250, 150, 120)), (100, 190))
        else:
            screen.blit(ff.render('Победа!', 1, (250, 150, 120)), (100, 190))
    else:
        pygame.time.delay(500)

    screen.blit(ff2.render('Управление клавишами <- и ->.', 1, (250, 250, 120)), (20, 450))
    screen.blit(ff2.render('Очки: %s' % (len(snake)-3), 1, (120, 250, 120)), (15, 5))

    window.blit(screen, (0, 0))
    pygame.display.flip()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit(0)
        if e.type == pygame.KEYDOWN:
            if vector > 0:
                if e.key == pygame.K_LEFT:
                    vector -= 1
                    if vector < 1:
                        vector = 6
                if e.key == pygame.K_RIGHT:
                    vector += 1
                    if vector > 6:
                        vector = 1