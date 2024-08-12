import pygame
from Particle import Particle
import random 
from sys import exit
import os
from double_slit import *
import math
from pygame.math import Vector2
from particles_manager import *
from PIL import Image
from osc_client import *
from floating_letters import *
from phrases import *
from wave_movement import *
from face_detection import *

#Text Animation
text_animation = None

osc_client = OscClient("127.0.0.1", 7400)

# Flags that can be changed
use_image = True  
use_collision = True
number_of_particles = 4000
particles_speed = 2
particles_radius = 2

# Control variables. Do not change
images = []
points = []
particles = []
box = []
WIDTH, HEIGHT = 0,0 
cap = None
particle_timer = 0
particle_interval = 1 
particles_manager = None
wave_movement = False

# Particle generation by collision
particles_gerenated = []
num_particles_gerenated = 0
index_next_to_alive = 0
last_activation_time = 0  # Timer para controlar a ativação das partículas
move_particle_status = False

class ImageTest:
    def __init__(self, path, width, height):
        self.path = path
        self.width = width
        self.height = height

def move_particles():
    for particle in particles_gerenated:
        particle.pos.x += (particle.original_pos.x - particle.pos.x) * 0.01
        particle.pos.y += (particle.original_pos.y - particle.pos.y) * 0.01
        pygame.draw.circle(screen, particle.color, (particle.pos.x, particle.pos.y), particle.radius)

def create_final_image(image_test):
    global particles_gerenated, num_particles_gerenated
    image = Image.open(image_test.path)
    image = image.resize((image_test.width,image_test.height), Image.Resampling.LANCZOS)
    image_data = image.load()
    num_particles_gerenated = image.width * image.height

    offset_x = (WIDTH - image.width) // 2
    offset_y = (HEIGHT - image.height) // 2
    for i in range(image.width):
        for j in range(image.height):
            color = image_data[i,j]
            r = random.randint(0,1)
            r2 = random.randint(0,1)
            if r == 1 and r2 == 1 and color != (0,0,0):
                position = (i + offset_x, j + offset_y)
                particle_generated = Particle(position, Vector2(0,0), 1, 1, color, False, False)
                particle_generated.alive = False
                particles_gerenated.append(particle_generated)                

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
    scale_x = screen_width - 10
    scale_y = screen_height - 10
    range_x = x_max - x_min
    range_y = y_max - y_min
    for i, e in enumerate(pontos_x):
        x = pontos_x[i]
        y = pontos_y[i]
        novo_x = ((x - x_min) / range_x) * scale_x
        novo_y = ((y - y_min) / range_y) * scale_y
        novos_pontos.append((novo_x, novo_y))
    return novos_pontos

def add_particle(position, direction, speed, radius, color_or_image, use_image):
    particles.append(Particle(position, direction, speed, radius, color_or_image, use_image))

def set_particles_speed(speed):
    for particle in particles:
        particle.speed = speed

half = 0
time_transition_to_final_image = 13000
time_transition_to_final_image_counter = 0

def draw_particles_final_image():
    move_particles()
    text_animation.draw_and_update(screen)

def draw_generated_particles(index_next_to_alive):
    for i in range(index_next_to_alive):
        particle = particles_gerenated[i]
        particle.update_pos()
        particle.draw(screen)

def create_generated_particles(result):
    osc_client.send_message("bands", random.randrange(0, 1024))
    osc_client.send_message("peak_width", random.randrange(0, 1024))
    to_alive_created_particle(result)
    x = random.uniform(result.pos.x - 20.0, result.pos.x + 20.0)
    y = random.uniform(result.pos.y - 20.0, result.pos.y + 20.0)
    to_alive_created_particle(Particle((x,y), result.dir, 1, 1, (0,0,0), False, False))
    x = random.uniform(result.pos.x - 40.0, result.pos.x + 40.0)
    y = random.uniform(result.pos.y - 40.0, result.pos.y + 40.0)
    to_alive_created_particle(Particle((x,y), result.dir, 1, 1, (0,0,0), False, False))
    x = random.uniform(result.pos.x - 80.0, result.pos.x + 80.0)
    y = random.uniform(result.pos.y - 80.0, result.pos.y + 80.0)
    to_alive_created_particle(Particle((x,y), result.dir, 1, 1, (0,0,0), False, False))
    to_alive_created_particle(result)

def to_alive_created_particle(result):
    global particles_gerenated, index_next_to_alive, move_particle_status, use_collision
    if index_next_to_alive < len(particles_gerenated):
        particles_gerenated[index_next_to_alive].pos = result.pos
        particles_gerenated[index_next_to_alive].dir = result.dir
        particles_gerenated[index_next_to_alive].speed = result.speed
        particles_gerenated[index_next_to_alive].radius = result.radius
        particles_gerenated[index_next_to_alive].alive = True
        index_next_to_alive += 1
    else:
        move_particle_status = True
        use_collision = False

def draw_particles():
    global time, index_next_to_alive, particles_gerenated, move_particle_status, half, use_collision, time_transition_to_final_image_counter, time_transition_to_final_image

    if move_particle_status:
        draw_particles_final_image()
        return
    
    particles_manager.clear_grid()

    draw_generated_particles(index_next_to_alive)

    for particle in particles:
        if wave_movement:
            update_wave_movement(time, particle)
        else:
            particle.update_pos()
        particle.draw(screen)
        particles_manager.add_particle_to_grid(particle)
        i, j = particles_manager.get_particle_position_on_grid(particle)
        result = particle.guidance(box, particles_manager.grid[i][j], use_collision if face_detected else False)
        if result != None and not move_particle_status:
            create_generated_particles(result)
      
    time += clock.get_time()
    if use_collision and face_detected:
        time_transition_to_final_image_counter += time//1000

    if time_transition_to_final_image_counter > time_transition_to_final_image: # esse trecho limita a geração de partículas a um tempo "time_transition_to_final_image". se passar disso, cria todas as partículas que faltam 
        qt = (int) ((len(particles_gerenated) - index_next_to_alive) // 2)
        for i in range(qt):
            particle = random.choice(particles)
            x = particle.pos.x
            y = particle.pos.y
            to_alive_created_particle(Particle((x,y), particle.dir, 1, 1, (0,0,0), False, False))

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

        if not face_detected:
            face_detected = process_face_detection()
            if face_detected:
                set_particles_speed(particles_speed)
            else:
                set_particles_speed(0)

        if len(particles) < number_of_particles:
            create_particle()
            create_particle()
            create_particle()
        else:
            wave_movement = not face_detected

        draw_particles()

        pygame.display.update()

    pygame.quit()
    cap.release()
    exit()

def config_text_animation(screen_width, screen_height, text_pos):
    global text_animation
    text_animation = TextAnimation(phrases[random.randint(0, len(phrases)-1)], screen_width, screen_height, text_pos)

if __name__ == "__main__":

    generate_images()

    pygame.init()

    # screen = pygame.display.set_mode((2560,1080))
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = pygame.display.get_surface().get_size()

    box = [0, WIDTH, 0, HEIGHT]

    image_test_1 = ImageTest("final_images/image19.jpg", WIDTH // 2, HEIGHT // 2)
    image_test_2 = ImageTest("final_images/image23.jpg", WIDTH, HEIGHT)
    image_test_3 = ImageTest("final_images/image17.jpg", WIDTH, HEIGHT)
    image_test_4 = ImageTest("final_images/image12.jpg", WIDTH - WIDTH // 3, HEIGHT - HEIGHT // 5)
    image_test_5 = ImageTest("final_images/image24.jpg", WIDTH - WIDTH // 12, HEIGHT)
    image_test_6 = ImageTest("final_images/image21.jpg", WIDTH - WIDTH // 4, HEIGHT - HEIGHT // 2)  # COGUMELOS
    image_test_7 = ImageTest("final_images/image7.png", WIDTH - WIDTH // 4, HEIGHT - HEIGHT // 10)
    image_test_8 = ImageTest("final_images/image8.jpg", WIDTH - WIDTH // 2, HEIGHT - HEIGHT // 3)  # ESTÁTUA AFRICANA
    image_test_9 = ImageTest("final_images/image20.jpg", WIDTH - WIDTH // 12, HEIGHT)
    image_test_10 = ImageTest("final_images/image25.jpeg", WIDTH - WIDTH // 5, HEIGHT - HEIGHT // 2)

    image_test = image_test_8

    create_final_image(image_test)
    half = len(particles_gerenated)//15

    # config_text_animation(WIDTH, HEIGHT, (WIDTH//2, HEIGHT//2 + HEIGHT//3))

    config_text_animation(WIDTH, HEIGHT, (WIDTH//2, (HEIGHT - image_test.height//2)+image_test.height//4))

    particles_manager = ParticlesManager(WIDTH, HEIGHT, 15)
    pygame.display.set_caption("Particle Simulation")
    clock = pygame.time.Clock()

    config_camera(WIDTH, HEIGHT)

    points_x, points_y = generate_points()
    x_min, x_max = -10, 10
    y_min, y_max = -4, 4
    points = transformar_pontos(points_x, points_y, x_min, x_max, y_min, y_max, WIDTH, HEIGHT)

    main()
