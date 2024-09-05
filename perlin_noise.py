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

# # Exemplo de estrutura da partícula
# class Particle:
#     def __init__(self, pos):
#         self.pos = pos
#         self.dir = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
#         self.speed = random.uniform(0.5, 2)
#         self.color = (255, 255, 255)

#     def update(self, time, center):
#         # Atualizar a direção da partícula usando Perlin Noise para afastamento do centro
#         self.dir = perlin_noise_direction(self, time, center)
        
#         # Atualizar a posição com base na direção e velocidade
#         self.pos += self.dir * self.speed

#     def draw(self, screen):
#         pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), 3)

# Inicialização do Pygame
# pygame.init()
# WIDTH, HEIGHT = 1521, 850
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# clock = pygame.time.Clock()

# # Centro da tela
# center = Vector2(WIDTH // 2, HEIGHT // 2)

# # Criando as partículas
# particles = [Particle(Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))) for _ in range(2000)]

# # Loop principal
# running = True
# time = 0
# while running:
#     time += 0.01  # Atualizar o tempo para o Perlin Noise

#     # Verificar eventos
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Atualizar a tela
#     screen.fill((0, 0, 0))

#     # Atualizar e desenhar as partículas
#     for particle in particles:
#         particle.update(time, center)  # Atualiza com Perlin Noise aplicado
#         particle.draw(screen)  # Desenha a partícula

#     pygame.display.flip()
#     clock.tick(60)

# pygame.quit()