import pygame
import math

class ParticlesManager:
    def __init__(self, screen_width, screen_height, grid_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.grid_size = grid_size
        self.rows_size = screen_width//grid_size 
        self.columns_size = screen_height//grid_size 
        self.grid = []

    def clear_grid(self):
        self.grid = [[[] for _ in range(self.columns_size)] for _ in range(self.rows_size)]

    def add_particle_to_grid(self, particle):
        i, j = self.get_particle_position_on_grid(particle)
        if 0 <= i < self.rows_size and 0 <= j < self.columns_size:
            self.grid[i][j].append(particle)

    def get_particle_position_on_grid(self, particle):
        x = particle.pos.x
        y = particle.pos.y
        i = int(x // self.grid_size)
        j = int(y // self.grid_size)
        # Ensure i and j are within the bounds
        i = max(0, min(self.rows_size - 1, i))
        j = max(0, min(self.columns_size - 1, j))
        return (i, j)
    
    def draw_partitions(self, screen):
        for i in range(self.rows_size + 1):
            x = i * self.grid_size
            pygame.draw.line(screen, (0, 0, 255), (x, 0), (x, self.screen_height))
        
        for j in range(self.columns_size + 1):
            y = j * self.grid_size
            pygame.draw.line(screen, (0, 0, 255), (0, y), (self.screen_width, y))