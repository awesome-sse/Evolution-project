import os
import time 
import numpy as np
import pygame
import random
import threading
import matplotlib.pyplot as plt
from classes import Field, Cell, Entity
from IPython.display import display, clear_output



class Evolution_field():
    
    def __init__(self, width=600, height=500, fps=80, field_width=30, field_height=30, keep_stats=False, stats=['age']) :
        # Init window
        pygame.init() 
        pygame.mixer.init()  # для звука

        #Colors
        self.COLOR_WHITE = (255,255,255) 
        self.COLOR_LIGHT = (180,180,180) 
        self.COLOR_DARK = (110,110,110) 

        #Game frame properties
        self.width = width  # ширина игрового окна
        self.height = height # высота игрового окна
        self.fps = fps # частота кадров в секунду

        # Main frame
        self.main_pos = (self.width / 1000, self.height / 1000)
        self.main_size = (self.width - 2 * self.width / 20, self.height - self.height / 1000)
        self.field_width = field_width
        self.field_height = field_height
        self.gridarray = np.arange(self.field_width * self.field_height).reshape((self.field_width, self.field_height))

        # Button quit
        self.quit_size = (50, 40) 
        smallfont = pygame.font.SysFont('Arial', 30) 
        self.text = smallfont.render('Quit', True, self.COLOR_WHITE) 

        # Init screen
        self.field = Field(size=(self.field_width, self.field_height))
        self.scr = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("Evolution Game")

        # Statistics
        self.keep_stats = keep_stats
        if self.keep_stats:
            self.stats = stats

    def set_entity(self, entity : Entity):
        self.field.add_entities(entity, entity.cell.x, entity.cell.y)

    def set_entity(self, entities : list[Entity]):
        for entity in entities:
            self.field.add_entities(entity, entity.cell.x, entity.cell.y)
    
    def draw_buttons(self):
        #Draw quit button
        mouse = pygame.mouse.get_pos() 
        self.quit_pos = (self.width - (self.width - self.main_size[0] + self.main_pos[0]) // 2 - self.quit_size[0] // 2, (self.main_size[1] - self.main_pos[1]) // 2)

        if self.quit_pos[0] <= mouse[0] <= self.quit_pos[0] + self.quit_size[0] and self.quit_pos[1] <= mouse[1] <= self.quit_pos[1] + self.quit_size[1]: 
                pygame.draw.rect(self.scr, self.COLOR_LIGHT, [*self.quit_pos, *self.quit_size]) 
        else: 
            pygame.draw.rect(self.scr, self.COLOR_DARK, [*self.quit_pos, *self.quit_size]) 
        
        self.scr.blit(self.text, self.quit_pos)

    def check_scr_size(self):
        current_widht, current_height = self.scr.get_size()

        if (current_widht != self.width) or (current_height != self.height):
            self.width = current_widht
            self.height = current_height

            self.scr = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

    def check_event(self):
        mouse = pygame.mouse.get_pos() 

        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                self.running = False     
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if self.quit_pos[0] <= mouse[0] <= self.quit_pos[0] + self.quit_size[0] and self.quit_pos[1] <= mouse[1] <= self.quit_pos[1] + self.quit_size[1]: 
                    self.running = False 

    def draw_main_frame(self):
        self.main_pos = (self.width / 1000, self.height / 1000)
        self.scr.fill((0, 0, 0))
        self.surface = pygame.surfarray.make_surface(self.field.cells()[self.gridarray])
        self.surface = pygame.transform.scale(self.surface, (self.width - 2 * self.width / 20, self.height - self.height / 1000))
        self.main_size = (self.width - 2 * self.width / 20, self.height - self.height / 1000)

        self.scr.blit(self.surface, self.main_pos)

    def event_loop(self):
        while self.running:
            self.check_event()
            self.check_scr_size()
            self.draw_main_frame()
            self.draw_buttons()
            pygame.display.update() 

            for entity in self.field.entities:
                entity.step(self.field)

            self.clock.tick(self.fps)

    def start(self):
        # Старт игры
        self.clock = pygame.time.Clock() 
        self.running = True

        # Statistics
        if self.keep_stats:
            lead_stats = threading.Thread(target=self.statistics)
            lead_stats.start()

        self.event_loop() # Start

        # After finish
        if self.keep_stats:
            lead_stats.join()
        
        pygame.display.flip()
        pygame.quit()

    def add_statistics(self):
        stats = np.zeros(len(self.stats))
        cnt = 0

        for entity in self.field.entities:
            for i, stat in enumerate(self.stats):
                stats[i] += np.float(entity.__dict__[stat])
            cnt += 1

        if cnt != 0:
            stats /= cnt
        
        for i, key in enumerate(self.statistics):
            self.statistics[key] = np.append(self.statistics[key], stats[i])


    def statistics(self):
        self.statistics = {}

        for stat in self.stats:
            if stat in Entity(Cell()).__dir__():
                self.statistics[stat] = np.array([], dtype=np.float)
            else:
                self.stats.remove(stat)

        rows = np.ceil(np.sqrt(len(self.stats))).astype(np.int)
        cols = np.ceil(len(self.stats) / rows).astype(np.int)

        plt.ion()
        plt.show()
        fig, axs = plt.subplots(rows, cols, sharey=True, squeeze=False)
        
        while self.running:
            self.add_statistics()

            for i, key in enumerate(self.statistics):
                y = self.statistics[key]
                x = np.arange(0, len(y), 1)
                axs[i // cols, i % cols].set_xlim(0, len(y))
                axs[i // cols, i % cols].cla()
                axs[i // cols, i % cols].plot(x, y)
                axs[i // cols, i % cols].set_title(key) 
    
            try:
                fig.canvas.draw()
                fig.canvas.flush_events()
                time.sleep(5)
            except:
                return
            

if __name__ == '__main__':

    entities = [Entity(Cell(x=10, y=10, color=(255, 10, 10))), 
             Entity(Cell(x=70, y=10, color=(10, 255, 10))),
             Entity(Cell(x=10, y=70, color=(10, 10, 255))),
             Entity(Cell(x=70, y=70, color=(100, 100, 100)))]
            
    evolution_game = Evolution_field(field_width=80, field_height=80, fps=80, keep_stats=True, stats=['age', 'energy', 'max_energy', 'energy_on_reproduction', 'energy_on_move', 'energy_from_sun', 'speed', 'mutation_chance', 'mutation_variance'])
    evolution_game.set_entity(entities)
    evolution_game.start()
    