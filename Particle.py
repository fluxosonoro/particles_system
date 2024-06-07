# Particle.py

from functions_geometric import euclidean_distance
import pygame
from pygame.math import Vector2

class Particle:
    def __init__(self, position, direction, speed, radius, color_or_image, use_image=False):
        self.pos = Vector2(position)
        self.dir = Vector2(direction).normalize()
        self.speed = speed
        self.radius = radius
        self.use_image = use_image
        if use_image:
            self.image = pygame.transform.scale(color_or_image, (2 * radius, 2 * radius))  # Resize image based on radius
        else:
            self.color = color_or_image
        self.collision_status = False
        
    def draw(self, screen):
        if self.use_image:
            screen.blit(self.image, (self.pos[0] - self.radius, self.pos[1] - self.radius))
        else:
            pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)

    def check_collision(self, use_collision, particles):
        if(use_collision):
            for particle in particles:
                if particle.pos != self.pos and self.is_collided(particle):
                    if not self.collision_status:
                        self.collision_status = True
                        self.collision_update_dir(particle)
                        
                        particle.collision_status = True
                        particle.collision_update_dir(self)

                        break
                    else:
                        break
            else:
                self.collision_status = False
    
    def guidance(self, box, particles, use_collision):
        self.boundary_update_dir(box)
        self.check_collision(use_collision, particles)

    def boundary_update_dir(self, box):
        if self.pos.x <= box[0] + self.radius and self.dir.x < 0:
            self.dir.x *= -1
        elif self.pos.x >= box[1] - self.radius and self.dir.x > 0:
            self.dir.x *= -1
        if self.pos.y <= box[2] + self.radius and self.dir.y < 0:
            self.dir.y *= -1
        elif self.pos.y >= box[3] - self.radius and self.dir.y > 0:
            self.dir.y *= -1

    def collision_update_dir(self, particle):
        x = self.pos.x - particle.pos.x
        y = self.pos.y - particle.pos.y
        if abs(x) >= abs(y):
            self.dir = Vector2(x / abs(x), y / abs(x)).normalize()
        else:
            self.dir = Vector2(x / abs(y), y / abs(y)).normalize()

    def is_collided(self, particle):
        return euclidean_distance(self.pos, particle.pos) <= self.radius + particle.radius

    def update_pos(self):
        self.pos += self.dir * self.speed
    
    def change_pos(self, x, y):
        self.pos = Vector2(x,y)
