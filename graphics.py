#graphics subclassing
from tkinter import *

class Tile:
    def __init__(self, x, y, size=10):
        #for drawing
        self.size = size
        self.x = x#top left corner
        self.y = y
        self.color = "pink"

        #tile properties
        self.foodChance = 1 #overall spawn rate
        self.foodTypes = None#list of available food classes to spawn
        self.foodDist = None #list of proportional food type spawn rates

        #multipliers for creatures travelling here
        self.speedMult = 1
        self.soundMult = 1
        self.visMult = 1
        self.fatigueMult = 1


    def draw(self, canvas):
        canvas.create_rectangle(self.x, self.y,
                self.x + self.size, self.y + self.size, fill=self.color )

class Grassland(Tile):
    def __init__(self, x, y, size=10):
        super().__init__(x, y, size)
        #for drawing
        self.color = "green"

        #tile properties
        self.foodChance = 10
        self.foodTypes = ["mid", "low"]
        self.foodDist = [0.1, 0.9]

        #multiplers for creatures travelling here

class Forest(Tile):
    pass

class Desert(Tile):
    pass

class Savanna(Tile):
    pass

class Marsh(Tile):
    pass


class Food:
    def __init__(self, x, y, size=10):
        self.x = x #center -BEWARE
        self.y = y
        self.size = size
        self.color = "pink"

        self.energy = 1

    def draw(self, canvas):
        canvas.create_oval(self.x - self.size/2, self.y - self.size/2,
                self.x + self.size/2, self.y + self.size/2, fill=self.color )

class LowFood(Food):
    def __init__(self, x, y, size=5):
        super().__init__(x, y, size)
        self.color = "green"
        self.energy = 0.2

class MidFood(Food):
    def __init__(self, x, y, size=5):
        super().__init__(x, y, size)
        self.color = "orange"
        self.energy = 1

class HiFood(Food):
    def __init__(self, x, y, size=5):
        super().__init__(x, y, size)
        self.color = "red"
        self.energy = 2

class Corpse(Food):
    def __init__(self, x, y, color, size=10):
        super().__init__(x, y, size)
        self.color = color
        self.energy = 10
