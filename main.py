# main.py

import pygame
from Particle import Particle
import random 
from sys import exit
import os
from dual_slit import *

images = []
points = []
WIDTH, HEIGHT = 1280, 720

def generate_images():
    path = "output_images_resized"
    valid_images = [".jpg",".gif",".png",".tga"]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() in valid_images:
            images.append(pygame.image.load(os.path.join(path, f)))

def generate_points():
    experiment = doubleSlit()
    experiment.distance_to_screen = 10
    experiment.slit_dist = 3 
    experiment.clear_screen()
    experiment.electron_beam(num_electrons=len(images))
    return experiment.get_positions()

def transformar_pontos(pontos_x, pontos_y, x_min, x_max, y_min, y_max, screen_width, screen_height):
    novos_pontos = []
    for i, e in enumerate(pontos_x):
        x = pontos_x[i]
        y = pontos_y[i]
        novo_x = ((x - x_min) / (x_max - x_min)) * screen_width
        novo_y = ((y - y_min) / (y_max - y_min)) * screen_height
        novos_pontos.append((novo_x, novo_y))
    return novos_pontos


def main():
    pygame.init()
   
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Particle Collider")
    clock = pygame.time.Clock()

    # Creating the background surface.
    bg = pygame.Surface((WIDTH, HEIGHT))
    bg.fill((20, 20, 20))

    # User choice: Use image for particles or not
    use_image = False  # Change to False to use simple colored circles

    directions = [-1, 1]

    # Create the particles using the Particle class.
    particles = []
    
    for i in range(len(images)):
        # pos = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        pos = points[i]
        dir = random.choice(directions)
        speed = 1
        radius = 5
        if use_image:
            particles.append(Particle(pos, dir, speed, radius, images[i], use_image=True))
        else:
            particles.append(Particle(pos, dir, speed, radius, (79, 187, 224), use_image=False))


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(bg, (0, 0))

        # Draw the particles.
        for particle in particles:
            particle.draw(screen)
            particle.guidance([0, WIDTH, 0, HEIGHT], particles)
            particle.update_pos()

        pygame.display.update()
        # clock.tick(30)

if __name__ == "__main__":
    generate_images()
    points_x, points_y = generate_points()
    x_min, x_max = -10, 10
    y_min, y_max = -4, 4
    points = transformar_pontos(points_x, points_y, x_min, x_max, y_min, y_max, WIDTH, HEIGHT)

    main()
