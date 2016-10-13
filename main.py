# -*- coding:utf-8 -*-

import pygame, sys
from random import choice
from hexagon import Hexagon

SIZE = (640, 480)

window = pygame.display.set_mode(SIZE)
screen = pygame.Surface(SIZE)
finally_background = pygame.Surface(SIZE)
finally_background.set_alpha(0)

pygame.font.init()
ff = pygame.font.Font(None, 120)
ff2 = pygame.font.Font(None, 24)

def generate_court():
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
    return hexes

def game():
    hexes = generate_court()
    snake = [(8, 18, 9),
             (8, 16, 8),
             (8, 14, 7)]

    vector = 1
    id = 8
    x = 14
    y = 7
    prey = 0
    alpha = 0
    done = False
    while not done:
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
                if len(snake) > 13:
                    vector = -1
                pygame.time.delay(100)
        else:
            vector = -1
        if id < 0 or id > 16 or y < 0 or y > 9:
            vector = -1

        for h in hexes:
            h.blit(screen, snake, prey)

        if vector == -1:
            if alpha < 100:
                alpha += 1
                finally_background.set_alpha(alpha)
            screen.blit(finally_background, (0, 0))
            if len(snake) < 13:
                screen.blit(ff.render('Поражение!', 1, (250, 150, 120)), (100, 190))
            else:
                screen.blit(ff.render('Победа!', 1, (250, 150, 120)), (150, 190))
        else:
            pygame.time.delay(500)

        screen.blit(ff2.render('Управление клавишами <- и ->.', 1, (250, 250, 120)), (20, 450))
        screen.blit(ff2.render('Выйти - Esc.', 1, (250, 250, 120)), (500, 450))
        screen.blit(ff2.render('Для победы наберите 10 очков', 1, (120, 250, 120)), (350, 5))
        screen.blit(ff2.render('Очки: %s' % (len(snake)-3), 1, (120, 250, 120)), (15, 5))

        window.blit(screen, (0, 0))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit(0)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    done = True
                if vector > 0:
                    if e.key == pygame.K_LEFT:
                        vector -= 1
                        if vector < 1:
                            vector = 6
                    if e.key == pygame.K_RIGHT:
                        vector += 1
                        if vector > 6:
                            vector = 1
                    if e.key == pygame.K_e:
                        if vector != 4:
                            vector = 1
                    if e.key == pygame.K_d:
                        if vector != 5:
                            vector = 2
                    if e.key == pygame.K_x:
                        if vector != 6:
                            vector = 3
                    if e.key == pygame.K_z:
                        if vector != 1:
                            vector = 4
                    if e.key == pygame.K_a:
                        if vector != 2:
                            vector = 5
                    if e.key == pygame.K_w:
                        if vector != 3:
                            vector = 6


                            
def menu():
    menu_font = pygame.font.Font(None, 80)
    while 1:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit(0)

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    game()
                if e.key == pygame.K_ESCAPE:
                    sys.exit(0)

        screen.fill((25, 50, 100))
        screen.blit(menu_font.render('Начать игру - Enter', 1, (255, 200, 100)), (60, 150))
        screen.blit(menu_font.render('Выйти - Esc', 1, (255, 200, 100)), (150, 250))

        window.blit(screen, (0, 0))
        pygame.display.flip()

if __name__ == '__main__':
    menu()
