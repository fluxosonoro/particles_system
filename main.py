import pygame
from Particle import Particle
import random 
from sys import exit
import os
from double_slit import *
import cv2
import mediapipe as mp

use_image = True 
use_camera = True
use_double_slit = True
use_face_interpolation = False
use_collision = False
number_of_particles = 200
particles_speed = 2
particles_radius = 5

images = []
points = []
particles = []
WIDTH, HEIGHT = 500, 500  # Definindo o tamanho padrão da janela

cap = None
face_mesh = None

# Variáveis para controlar o tempo de criação de partículas
particle_timer = 0
particle_interval = 100  # Intervalo de 1 segundo para a criação de partículas (em milissegundos)

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
        novo_x = ((x - x_min) / (x_max - x_min)) * (screen_width - 10)
        novo_y = ((y - y_min) / (y_max - y_min)) * (screen_height - 10)
        novos_pontos.append((novo_x, novo_y))
    return novos_pontos

def add_particle(position, direction, speed, radius, color_or_image, use_image):
    particles.append(Particle(position, direction, speed, radius, color_or_image, use_image))

def process_face_detection(screen):
    global cap, face_mesh
    ret, camera_image = cap.read()
    if ret:
        camera_image = cv2.resize(camera_image, (WIDTH, HEIGHT))  # Redimensionar a imagem da câmera para o tamanho da janela
        camera_surf = pygame.image.frombuffer(camera_image.tobytes(), camera_image.shape[1::-1], "BGR")
        screen.blit(camera_surf, (0, 0))

    landmarks = []

    results = face_mesh.process(camera_image)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for landmark in face_landmarks.landmark:
                x = int(landmark.x * WIDTH)  # Usar WIDTH em vez de camera_image.shape[1]
                y = int(landmark.y * HEIGHT)  # Usar HEIGHT em vez de camera_image.shape[0]
                landmarks.append((x, y))

        if use_face_interpolation:
            for i, (particle, landmark) in enumerate(zip(particles, landmarks)):
                particle.pos.x = (1 - 0.1) * particle.pos.x + 0.1 * landmark[0]
                particle.pos.y = (1 - 0.1) * particle.pos.y + 0.1 * landmark[1] 

    for landmark in landmarks:
        pygame.draw.circle(screen, (255, 0, 0), landmark, 1)

def main():
    global number_of_particles
    global particles
    global cap
    global particle_timer

    bg = pygame.Surface((WIDTH, HEIGHT))
    bg.fill((20, 20, 20))

    directions = [-1, 1]
 
    if use_image:
        number_of_particles = len(images)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        if use_camera:
            process_face_detection(screen)
        else:
            screen.blit(bg, (0, 0))

        current_time = pygame.time.get_ticks()
        if current_time - particle_timer > particle_interval:
            particle_timer = current_time
            if len(particles) < number_of_particles:
                if use_double_slit:
                    pos = points[len(particles)]
                else:
                    pos = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
                    
                dir = random.choice(directions)
                speed = particles_speed
                radius = particles_radius
                if use_image:
                    add_particle(pos, dir, speed, radius, images[len(particles)], use_image=True)
                else:
                    add_particle(pos, dir, speed, radius, (79, 187, 224), use_image=False)

        for particle in particles:
            particle.draw(screen)
            particle.guidance([0, WIDTH, 0, HEIGHT], particles, use_collision)
            particle.update_pos()

        clock.tick(30)
        pygame.display.update()

    pygame.quit()
    if use_camera:
        cap.release()
    exit()

def config_camera():
    global cap, face_mesh
    if use_camera:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

if __name__ == "__main__":

    generate_images()

    pygame.init()

    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = pygame.display.get_surface().get_size()
    pygame.display.set_caption("Particle Simulation")
    clock = pygame.time.Clock()

    config_camera()

    points_x, points_y = generate_points()
    x_min, x_max = -10, 10
    y_min, y_max = -4, 4
    points = transformar_pontos(points_x, points_y, x_min, x_max, y_min, y_max, WIDTH, HEIGHT)

    main()
