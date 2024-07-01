import pygame
import math
import random

# Inicializar o Pygame
pygame.init()

# Definir parâmetros da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Onda Longitudinal')

# Definir cores
branco = (255, 255, 255)
preto = (0, 0, 0)
azul = (0, 0, 255)

# Definir parâmetros da onda
A = 20  # Amplitude da onda
T = 2000  # Período da onda (tempo para um ciclo completo em milissegundos)
wavelength = 100  # Comprimento de onda

# Gerar partículas em posições aleatórias
num_particulas = 1000
particulas = [(random.randint(0, largura), random.randint(0, altura)) for _ in range(num_particulas)]

# Função para atualizar a posição das partículas
def atualizar_posicoes(t):
    novas_posicoes = []
    for (x, y) in particulas:
        # Calcular o deslocamento da partícula usando a função de onda longitudinal
        deslocamento = A * math.sin((2 * math.pi / T) * t - (2 * math.pi / wavelength) * x)
        novo_x = x + deslocamento
        novas_posicoes.append((novo_x, y))
    return novas_posicoes

# Loop principal
rodando = True
tempo = 0
clock = pygame.time.Clock()

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Atualizar a posição das partículas
    posicoes_atualizadas = atualizar_posicoes(tempo)
    tempo += clock.get_time()

    # Desenhar fundo
    tela.fill(branco)

    # Desenhar partículas
    for (x, y) in posicoes_atualizadas:
        pygame.draw.circle(tela, azul, (int(x), int(y)), 5)

    # Atualizar a tela
    pygame.display.flip()

    # Controlar a taxa de frames
    clock.tick(60)

# Finalizar o Pygame
pygame.quit()
