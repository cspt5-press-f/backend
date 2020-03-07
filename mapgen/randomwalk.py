"""
Random Walk

Yield a generator to produce coordinates along 2-D random walk.
"""

import numpy as np
import random

def generate_coordinates():
    x = 0
    y = 0

    while True:
        val = random.randint(1, 4) 
        if val == 1: 
            x += 1
        elif val == 2: 
            x -= 1
        elif val == 3: 
            y += 1
        else: 
            y -= 1

        yield x,y

class RandomWalk():
    def __init__(self, size):
        self.generator = generate_coordinates()
        self.coordinates = self.build_map(size)

    def build_map(self, size):
        new_coordinates = [0, 0]
        while len(new_coordinates) < size:
            temp_coord = next(self.generator)
            if temp_coord in new_coordinates:
                continue
            else:
                new_coordinates.append(temp_coord)
        return new_coordinates


if __name__ == "__main__":
    walk = RandomWalk(size=10)
    print(walk.coordinates)