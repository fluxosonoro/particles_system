import pygame
from pygame.math import Vector2
import math
import random

class Lightning:
    def __init__(self, dir, pos, speed):
        self.dir = dir
        self.pos = pos
        self.initial_pos = Vector2(pos)  # Guarda a posição inicial para calcular o comprimento
        self.speed = speed

class Explosion:

    def create_lightning(self):
            angle = random.uniform(0, 2 * math.pi)
            dir = Vector2(math.cos(angle), math.sin(angle))
            dir.normalize()
            lightning_pos = self.position + dir * self.initial_speed
            speed = random.uniform(3, self.speed)
            return Lightning(dir, lightning_pos, speed)

    def create_lightnings(self, n):
        for i in range(n):
            self.lightnings.append(self.create_lightning())
            self.particles.append(self.create_lightning())  #Atualmente Particles são Lightning. Se necessário, mudar depois

    def __init__(self, position, initial_speed=10, n=10, max_length=300, deceleration=0.4, color=(216,211,165)):
        self.initial_speed = initial_speed
        self.speed = initial_speed
        self.position = Vector2(position)
        self.n = n
        self.color = color
        self.lightnings = []
        self.particles = []
        self.max_length = max_length
        self.create_lightnings(n)
        self.deceleration = deceleration
        self.active = True  # Indica se a explosão ainda está ativa

    def draw(self, screen):
        if self.active:
            for lightning in self.lightnings:
                pygame.draw.aaline(screen, self.color, self.position, lightning.pos)
            
            for particle in self.particles:
                pygame.draw.circle(screen, self.color, particle.pos, 1)

    def change_color(self):
        r, g, b = self.color
        dec_amount = 1  # Valor de decremento de cor
        r = max(0, r - dec_amount)
        g = max(0, g - dec_amount)
        b = max(0, b - dec_amount)
        self.color = (r, g, b)


    def update(self, dt):
        if self.active:
            self.change_color()
            for i in range(self.n):
                lightning = self.lightnings[i]
                particle = self.particles[i]

                lightning.speed -= self.deceleration 
                lightning.speed = max(1, lightning.speed)  
                particle.speed -= self.deceleration 
                particle.speed = max(1, particle.speed) 
                
                lightning.pos += lightning.dir * lightning.speed 
                particle.pos += particle.dir * particle.speed 

                length = lightning.pos.distance_to(self.position)
                if length >= self.max_length:
                    self.active = False
                    break  # Para o loop se qualquer raio atingir o comprimento máximo
