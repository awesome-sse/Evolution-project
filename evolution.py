import os
import time 
import numpy as np
import pygame
import random
from classes import Field, Cell, Entity

WIDTH = 600  # ширина игрового окна
HEIGHT = 500 # высота игрового окна
FPS = 80 # частота кадров в секунду

curr_width = WIDTH
curr_height = HEIGHT

color_white = (255,255,255) 
color_light = (180,180,180) 
color_dark = (110,110,110) 

# создаем игру и окно
pygame.init()
pygame.mixer.init()  # для звука
scr = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
running = True

# Button quit
smallfont = pygame.font.SysFont('Arial',30) 
text = smallfont.render('Quit' , True , color_white) 
q_pos = (WIDTH - WIDTH / 10 + 3, HEIGHT - HEIGHT / 20)
quit_size = (50, 40) 

# Main frame
main_pos = (WIDTH / 1000, HEIGHT / 1000)
main_size = (WIDTH - 2 * WIDTH / 20, HEIGHT - HEIGHT / 1000)
gridarray = np.arange(30 * 30).reshape((30, 30))

f = Field((30, 30))

x = 10
y = 10
f.add_entities(Entity(Cell(x, y, (100, 255, 100)), max_age=30), x, y)
# f.add_entities(Entity(Cell(x + 3, y - 3, (10, 255, 10))), x + 3, y - 3)
# f.add_entities(Entity(Cell(x - 3, y - 3, (10, 255, 10))), x - 3, y - 3)
# f.add_entities(Entity(Cell(x + 3, y + 3, (10, 255, 10))), x + 3, y + 3)

def draw_buttons(src, witgh, height):
    global q_pos
    #Draw quit button

    mouse = pygame.mouse.get_pos() 
    q_pos = (witgh - witgh / 10 + 3, height - height / 20)

    if q_pos[0] <= mouse[0] <= q_pos[0] + quit_size[0] and q_pos[1] <= mouse[1] <= q_pos[1] + quit_size[1]: 
            pygame.draw.rect(scr, color_light, [*q_pos, *quit_size]) 
    else: 
        pygame.draw.rect(scr, color_dark, [*q_pos, *quit_size]) 

    scr.blit(text, q_pos)

def check_event():
    global running

    mouse = pygame.mouse.get_pos() 

    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            running = False     
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if q_pos[0] <= mouse[0] <= q_pos[0] + quit_size[0] and q_pos[1] <= mouse[1] <= q_pos[1] + quit_size[1]: 
                running = False 


def check_scr_size(scr):
    global curr_width, curr_height, main_pos

    c_widht, c_height = scr.get_size()

    if (c_widht != curr_width) or (c_height != curr_height):
        curr_width = c_widht
        curr_height = c_height

        scr = pygame.display.set_mode((curr_width, curr_height), pygame.RESIZABLE)
        

def draw_main_frame(scr, witgh, height):
    global surface

    main_pos = (witgh / 1000, height / 1000)
    scr.fill((0, 0, 0))
    surface = pygame.surfarray.make_surface(f.cells()[gridarray])
    surface = pygame.transform.scale(surface, (witgh - 2 * witgh / 20, height - height / 1000))

    scr.blit(surface, main_pos)


def event_loop():

    while running:
        check_event()
        check_scr_size(scr)
        draw_main_frame(scr, curr_width, curr_height)
        draw_buttons(scr, curr_width, curr_height)
        pygame.display.update() 

        for entity in f.entities:
            entity.step(f)

        clock.tick(FPS)


if __name__ == '__main__':
    event_loop()
    pygame.display.flip() 