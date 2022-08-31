import numpy as np
from torch import EnumType
from classes import * 

class Field():
    def __init__(self, size = (50, 50)):  
        self.size = size 
        self.field = np.zeros(size, dtype=object)
        self.entities = []

    def add_entities(self, entity = None, x = -1, y = -1):
        if x < 0 or y < 0:
            x = np.random.randint(0, self.size[0])
            y = np.random.randint(0, self.size[1])
        
        self.field[x, y] = entity
        self.entities.append(entity)

        return (x, y)

    def cells(self):
        cells = []
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if not isinstance(self.field[i, j], Entity):
                    cells.append((255, 255, 255))
                else:
                    cells.append(self.field[i, j].cell.color)
        
        return np.array(cells)


class Cell:
    def __init__(self, x = 0, y = 0, color = (10, 255, 10)):  
        self.x = x  
        self.y = y  
        self.color = color


class Entity:

    def __init__(self, cell, max_energy = 100, energy = 50, age = 0, max_age = 10, 
                    energy_on_reproduction = 20, energy_on_move = 10, energy_from_sun = 30,
                    speed = 1, mutation_chance = 0.05, mutation_variance = 0.1):
        self.max_energy = max_energy
        self.energy = energy
        self.age = age
        self.max_age = max_age
        self.energy_on_reproduction = energy_on_reproduction
        self.energy_on_move = energy_on_move
        self.energy_from_sun = energy_from_sun
        self.cell = cell
        #New
        self.speed = speed
        self.mutation_chance = mutation_chance
        self.mutation_variance = mutation_variance

    def mutation(self, entity):

        for attr, val in self.__dict__.items():
            if attr == 'cell':
                r = np.int(self.cell.color[0] + self.cell.color[0] * np.random.normal(0, self.mutation_variance)) if np.random.sample() <= self.mutation_chance else self.cell.color[0]
                g = np.int(self.cell.color[1] + self.cell.color[1] * np.random.normal(0, self.mutation_variance)) if np.random.sample() <= self.mutation_chance else self.cell.color[1]
                b = np.int(self.cell.color[2] + self.cell.color[2] * np.random.normal(0, self.mutation_variance)) if np.random.sample() <= self.mutation_chance else self.cell.color[2]

                entity.cell.color = (max(min(r, 255), 0), max(min(g, 255), 0), max(min(b, 255), 0))

            elif attr not in ('age'):
                entity.__dict__[attr] = max(val + val * np.random.normal(0, self.mutation_variance), 0) if np.random.sample() <= self.mutation_chance else self.__dict__[attr]
        
        return entity
                

    def move(self, field):

        def move_left(self):
            field.field[self.cell.x, self.cell.y] = 0
            field.field[self.cell.x - 1, self.cell.y] = self
            self.cell.x -= 1
            self.energy -= self.energy_on_move
        
        def move_right(self):
            field.field[self.cell.x, self.cell.y] = 0
            field.field[self.cell.x + 1, self.cell.y] = self
            self.cell.x += 1
            self.energy -= self.energy_on_move
        
        def move_up(self):
            field.field[self.cell.x, self.cell.y] = 0
            field.field[self.cell.x, self.cell.y - 1] = self
            self.cell.y -= 1
            self.energy -= self.energy_on_move

        def move_down(self):
            field.field[self.cell.x, self.cell.y] = 0
            field.field[self.cell.x, self.cell.y + 1] = self
            self.cell.y += 1
            self.energy -= self.energy_on_move

        for _ in range(np.around(self.speed).astype(np.int)):
            actions = []
            if self.cell.x > 0 and field.field[self.cell.x - 1, self.cell.y] == 0:
                actions.append(move_left)
            if self.cell.x < field.size[0] - 1 and field.field[self.cell.x + 1, self.cell.y] == 0:
                actions.append(move_right)
            if self.cell.y > 0 and field.field[self.cell.x, self.cell.y - 1] == 0:
                actions.append(move_up)
            if self.cell.y < field.size[1] - 1 and field.field[self.cell.x, self.cell.y + 1] == 0: 
                actions.append(move_down)
            if len(actions) == 0:
                continue
            else:
                actions[np.random.randint(0, len(actions))](self)


    def reproduction(self, field):

        def rep_left(self):
            field.field[self.cell.x - 1, self.cell.y] = self.mutation(Entity(Cell(self.cell.x - 1, self.cell.y)))
            field.entities.append(field.field[self.cell.x - 1, self.cell.y])
            self.energy -= self.energy_on_reproduction
        
        def rep_right(self):
            field.field[self.cell.x + 1, self.cell.y] = self.mutation(Entity(Cell(self.cell.x + 1, self.cell.y)))
            field.entities.append(field.field[self.cell.x + 1, self.cell.y])
            self.energy -= self.energy_on_reproduction

        def rep_up(self):
            field.field[self.cell.x, self.cell.y - 1] = self.mutation(Entity(Cell(self.cell.x, self.cell.y - 1)))
            field.entities.append(field.field[self.cell.x, self.cell.y - 1])
            self.energy -= self.energy_on_reproduction

        def rep_down(self):
            field.field[self.cell.x, self.cell.y + 1] = self.mutation(Entity(Cell(self.cell.x, self.cell.y + 1)))
            field.entities.append(field.field[self.cell.x, self.cell.y + 1])
            self.energy -= self.energy_on_reproduction

        actions = []
        if self.cell.x > 0 and field.field[self.cell.x - 1, self.cell.y] == 0:
            actions.append(rep_left)
        if self.cell.x < field.size[0] - 1 and field.field[self.cell.x + 1, self.cell.y] == 0:
            actions.append(rep_right)
        if self.cell.y > 0 and field.field[self.cell.x, self.cell.y - 1] == 0:
            actions.append(rep_up)
        if self.cell.y < field.size[1] - 1 and field.field[self.cell.x, self.cell.y + 1] == 0: 
            actions.append(rep_down)
        if len(actions) == 0:
            return
        else:
            actions[np.random.randint(0, len(actions))](self)


    def plus_energy(self, field=None):
        self.energy = min(self.energy + self.energy_from_sun, self.max_energy)

    def sleep(self, field=None):
        return

    def step(self, field):
        actions = [self.plus_energy, self.sleep]
        if self.energy >= self.energy_on_move:
            actions.append(self.move)
        if self.energy >= self.energy_on_reproduction:
            actions.append(self.reproduction)

        actions[np.random.randint(0, len(actions))](field)
        self.age += 1

        if self.energy <= 0 or self.age >= self.max_age:
            field.field[self.cell.x, self.cell.y] = 0
            field.entities.remove(self)

if __name__ == '__main__':
    e = Entity(Cell())
    print(Entity(Cell()).__dir__())