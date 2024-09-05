import pygame
import random
import math
from pygame.math import Vector2
import noise  # Importa a biblioteca de Perlin Noise

# Função que retorna a direção para fora do centro da tela, aplicando uma distorção com Perlin Noise
def perlin_noise_direction(particle, time, center):
    # Vetor da partícula até o centro da tela
    direction = particle.pos - center
    
    # Normaliza o vetor para obter a direção
    direction = direction.normalize()

    # Aplicar o Perlin Noise para distorcer levemente a direção
    noise_value_x = noise.pnoise3(particle.pos.x * 0.08, particle.pos.y * 0.08, time)
    noise_value_y = noise.pnoise3(particle.pos.y * 0.08, particle.pos.x * 0.08, time)
    
    distortion_x = noise_value_x * 0.4  # Ajuste para controlar a intensidade da distorção
    distortion_y = noise_value_y * 0.4

    # Modificar a direção da partícula com o ruído Perlin
    distorted_direction = Vector2(direction.x + distortion_x, direction.y + distortion_y)
    
    # Normalizar a direção resultante
    return distorted_direction.normalize()