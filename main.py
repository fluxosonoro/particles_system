import pygame
from Particle import Particle
import random 
from sys import exit
import os
from double_slit import *
import cv2
import mediapipe as mp
import math
from pygame.math import Vector2
from particles_manager import *
from explosion import *

# Flags that can be changed
use_image = True  
use_collision = True
number_of_particles = 4000
particles_speed = 2
particles_radius = 2

# Wave parameters
A = 10  # Wave amplitude
T = 1000  # Wave period (time for one complete cycle in milliseconds)
wavelength = 100 
time = 0
wave_movement_velocity = 0.2

# Control variables. Do not change
images = []
points = []
particles = []
box = []
WIDTH, HEIGHT = 0,0 
cap = None
face_mesh = None
face_detected = False
particle_timer = 0
particle_interval = 1 
particles_manager = None
wave_movement = False

def generate_images():
    path = "output_images_resized"
    valid_images = [".jpg",".gif",".png",".tga"]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() in valid_images:
            images.append(pygame.image.load(os.path.join(path, f)))
            images.append(pygame.image.load(os.path.join(path, f)))

def generate_points():
    global number_of_particles
    experiment = doubleSlit()
    experiment.distance_to_screen = 10
    experiment.slit_dist = 3 
    experiment.clear_screen()
    if use_image:
        number_of_particles = len(images)
    experiment.electron_beam(num_electrons=number_of_particles)
    return experiment.get_positions()

def transformar_pontos(pontos_x, pontos_y, x_min, x_max, y_min, y_max, screen_width, screen_height):
    novos_pontos = []
    for i, e in enumerate(pontos_x):
        x = pontos_x[i]
        y = pontos_y[i]
        novo_x = ((x - x_min) / (x_max - x_min)) * (screen_width - 10)
        novo_y = ((y - y_min) / (y_max - y_min)) * (screen_height - 10)
        novos_pontos.append((novo_x, novo_y))
    return novos_pontos

def add_particle(position, direction, speed, radius, color_or_image, use_image):
    particles.append(Particle(position, direction, speed, radius, color_or_image, use_image))

def set_particles_speed(speed):
    for particle in particles:
        particle.speed = speed

def process_face_detection(screen):
    global cap, face_mesh, face_detected
    ret, camera_image = cap.read()

    results = face_mesh.process(camera_image)
    
    if results.multi_face_landmarks:
        face_detected = True
        set_particles_speed(particles_speed)
    else:
        face_detected = False
        set_particles_speed(0)

def draw_particles(dt):
    global time
    particles_manager.clear_grid()
    for particle in particles:
        if wave_movement:
            update_wave_movement(time, particle)
        else:
            particle.update_pos()
        particle.draw(screen, dt)
        particles_manager.add_particle_to_grid(particle)
        i, j = particles_manager.get_particle_position_on_grid(particle)
        particle.guidance(box, particles_manager.grid[i][j], use_collision if face_detected else False)
    
    time += clock.get_time()

def update_wave_movement(t, particle):
    x = particle.original_pos.x
    deslocamento = A * math.sin((2 * math.pi / T) * t - (2 * math.pi / wavelength) * x)
    particle.pos.x += deslocamento * wave_movement_velocity

def create_particles():
    for _ in range(number_of_particles):
        create_particle()

def create_particle():
    if len(particles) < number_of_particles:
        pos = points[len(particles)]
        angle = random.uniform(0, 2 * math.pi)  
        dir = Vector2(math.cos(angle), math.sin(angle)).normalize()
        speed = particles_speed if face_detected else 0
        radius = particles_radius
        if use_image:
            add_particle(pos, dir, speed, radius, images[len(particles)], use_image=True)
        else:
            add_particle(pos, dir, speed, radius, (255, 255, 255), use_image=False)

def main():
    global number_of_particles, particles, cap, face_detected, wave_movement, time

    bg = pygame.Surface((WIDTH, HEIGHT))
    bg.fill((0, 0, 0))
 
    if use_image:
        number_of_particles = len(images)

    # create_particles()
    
    running = True
    while running:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.blit(bg, (0, 0))

        process_face_detection(screen)

        if len(particles) < number_of_particles:
            create_particle()
            create_particle()
            create_particle()
        else:
            wave_movement = not face_detected

        draw_particles(dt)

        pygame.display.update()

    pygame.quit()
    cap.release()
    exit()

def config_camera():
    global cap, face_mesh
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

if __name__ == "__main__":

    generate_images()

    pygame.init()

    # screen = pygame.display.set_mode((2560,1080))
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = pygame.display.get_surface().get_size()

    box = [0, WIDTH, 0, HEIGHT]

    particles_manager = ParticlesManager(WIDTH, HEIGHT, 15)
    pygame.display.set_caption("Particle Simulation")
    clock = pygame.time.Clock()

    config_camera()

    points_x, points_y = generate_points()
    x_min, x_max = -10, 10
    y_min, y_max = -4, 4
    points = transformar_pontos(points_x, points_y, x_min, x_max, y_min, y_max, WIDTH, HEIGHT)

    main()
