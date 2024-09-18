from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image
import random
import noise
import math
from osc_client import OscClient
from particles_manager import ParticlesManager
from face_detection import FaceDetection
from phrases import phrases
from floating_letters import TextAnimation
from wave_movement import update_wave_movement
from double_slit import doubleSlit
from Particle import *
import os
import time

def draw_circle(x, y, radius, color):
    glColor3f(color[0]/255.0, color[1]/255.0, color[2]/255.0)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for angle in np.linspace(0, 2 * math.pi, num=32):
        glVertex2f(x + math.cos(angle) * radius, y + math.sin(angle) * radius)
    glEnd()

def create_window(width, height, title="Particle Simulation"):
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(title.encode('ascii'))

class ImageTest:
    def __init__(self, path, width, height):
        self.path = path
        self.width = width
        self.height = height

    @staticmethod
    def get_list(WIDTH, HEIGHT):
        image_test_1 = ImageTest("final_images/image19.jpg", WIDTH // 2, HEIGHT // 2)
        image_test_2 = ImageTest("final_images/image23.jpg", WIDTH // 2, HEIGHT // 2)
        image_test_3 = ImageTest("final_images/image17.jpg", WIDTH  - WIDTH // 3, HEIGHT // 2)
        image_test_4 = ImageTest("final_images/image12.jpg", WIDTH - WIDTH // 2, HEIGHT - HEIGHT // 3)
        image_test_5 = ImageTest("final_images/image24.jpg", WIDTH - WIDTH // 4, HEIGHT // 2)
        image_test_6 = ImageTest("final_images/image21.jpg", WIDTH - WIDTH // 3, HEIGHT - HEIGHT // 2)  # COGUMELOS
        image_test_7 = ImageTest("final_images/image7.png", WIDTH - WIDTH // 2, HEIGHT - HEIGHT // 2)
        image_test_8 = ImageTest("final_images/image8.jpg", WIDTH - WIDTH // 2, HEIGHT - HEIGHT // 3)  # ESTÁTUA AFRICANA
        image_test_9 = ImageTest("final_images/image20.jpg", WIDTH - WIDTH // 3, HEIGHT // 2)
        return [image_test_1, image_test_2, image_test_3, image_test_4, image_test_5, image_test_6, image_test_7, image_test_8, image_test_9]


class ParticleSimulation:

    def init_sound_variables(self):
        self.peak_width_1 = 400
        self.peak_width_2 = 394
        self.bands = 146

    def init_text_variables(self):
        self.text_animation = None

    def init_particles_variables(self):
        self.use_image = True
        self.use_collision = True
        self.number_of_particles = 4000
        self.particles_speed = 2
        self.particles_radius = 2
        self.particles = []
        self.particle_timer = 0
        self.particle_interval = 1
        self.wave_movement = False

    def init_double_slit_points(self):
        points_x, points_y = self.generate_points()
        x_min, x_max = -10, 10
        y_min, y_max = -4, 4
        self.points = self.transformar_pontos(points_x, points_y, x_min, x_max, y_min, y_max, self.WIDTH, self.HEIGHT)

    def init_particles_from_collision_variables(self):
        self.particles_from_collision = []
        self.num_particles_from_collision = 0
        self.index_next_to_alive = 0
        self.last_activation_time = 0  # Timer para controlar a ativação das partículas
        self.move_particle_status = False
        self.restart_status = False

    def init_background(self):
        self.bg_color = (0, 0, 0)

    def init_restart_transition_variables(self):
        self.speed_particle_restart = 2
        self.speed_incrementer_particle_restart = 0.01
        self.time_transition_to_final_image = 13000
        self.time_transition_to_final_image_counter = 0
        self.count_particles_to_restart = 0

    def init_timer(self):
        self.timer = 0

    def choise_final_image(self):
        self.image_test = random.choice(self.images_test_list)
    
    def config_text_animation(self, screen_width, screen_height, text_pos):
        self.text_animation = TextAnimation(phrases[random.randint(0, len(phrases)-1)], screen_width, screen_height, text_pos)

    def init_timer(self):
        self.timer = 0
        self.clock = time.time()  # Inicialize o atributo clock aqui

    def init_variables(self):
        self.face_detector.init_variables()
        self.init_text_variables()
        self.init_sound_variables()
        self.init_particles_variables()
        self.init_particles_from_collision_variables()
        self.init_restart_transition_variables()
        self.init_timer()
        self.choise_final_image()
        self.create_final_image(self.image_test)
        self.half = len(self.particles_from_collision) // 15
        self.config_text_animation(self.WIDTH, self.HEIGHT, (self.WIDTH // 2, (self.HEIGHT - self.image_test.height // 2) + self.image_test.height // 4))
        self.init_double_slit_points()
        self.init_background()
        self.init_timer()

        if self.use_image:
            self.number_of_particles = len(self.images)

        self.running = True

    def create_osc_client(self):
        # Assumindo que OscClient é uma classe que precisa ser adaptada para PyOpenGL
        self.osc_client = OscClient("127.0.0.1", 7400)

    def create_screen(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(800, 600)
        self.window = glutCreateWindow("Particle Simulation")
        self.WIDTH, self.HEIGHT = 800, 600
        self.center = [self.WIDTH // 2, self.HEIGHT // 2]
        self.box = [0, self.WIDTH, 0, self.HEIGHT]

    def create_face_detector(self):
        # Assumindo que FaceDetection é uma classe que pode ser substituída
        self.face_detector = FaceDetection()
        self.face_detector.config_camera(self.WIDTH, self.HEIGHT)

    def create_images_for_test(self):
        self.images_test_list = ImageTest.get_list(self.WIDTH, self.HEIGHT)

    def create_particles_manager(self):
        self.particles_manager = ParticlesManager(self.WIDTH, self.HEIGHT, 15)

    def init_gl(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Define a cor de fundo
        glEnable(GL_DEPTH_TEST)  # Habilita o teste de profundidade
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.WIDTH, 0, self.HEIGHT)  # Define a projeção ortográfica
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glPointSize(2)  # Define o tamanho do ponto

    def __init__(self):
        # glutInit()  # Inicializar a janela OpenGL
        self.create_screen()
        self.create_osc_client()
        self.create_face_detector()
        self.create_images_for_test()
        self.create_particles_manager()
        self.generate_images()
        self.init_gl()  # Inicialize o OpenGL
        self.init_variables()

    def generate_images(self):
        self.images = []
        path = "output_images_resized"
        valid_images = [".jpg", ".gif", ".png", ".tga"]

        for f in os.listdir(path):
            ext = os.path.splitext(f)[1]
            if ext.lower() in valid_images:
                img_path = os.path.join(path, f)
                
                # Carregar imagem com Pillow
                img = Image.open(img_path)
                img = img.transpose(Image.FLIP_TOP_BOTTOM)  # Inverter a imagem no eixo y, pois OpenGL usa coordenadas diferentes
                
                img_data = img.convert("RGBA").tobytes()  # Converter para RGBA e pegar os bytes da imagem
                
                # Criar textura no OpenGL
                texture_id = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, texture_id)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

                # Especificar a textura usando os dados da imagem
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

                # Desvincular a textura
                glBindTexture(GL_TEXTURE_2D, 0)

                # Adicionar o id da textura à lista de imagens
                self.images.append(texture_id)
                self.images.append(texture_id)


    def create_final_image(self, image_test):
        image = Image.open(image_test.path)
        image = image.resize((image_test.width, image_test.height), Image.Resampling.LANCZOS)
        image_data = np.array(image)
        self.num_particles_from_collision = image.width * image.height

        offset_x = (self.WIDTH - image.width) // 2
        offset_y = (self.HEIGHT - image.height) // 2
        for i in range(image.width):
            for j in range(image.height):
                color = image_data[j, i]
                if all(color != (0, 0, 0)):
                    position = (i + offset_x, j + offset_y)
                    particle_generated = Particle(position, Vector2(0, 0), 1, 1, color, False, False)
                    particle_generated.alive = False
                    self.particles_from_collision.append(particle_generated)

    def move_particles(self):
        self.restart_status = False
        cont = 0

        glBegin(GL_POINTS)

        for particle in self.particles_from_collision:
            dx = (particle.original_pos.x - particle.pos.x)
            dy = (particle.original_pos.y - particle.pos.y)
            particle.pos.x += dx * 0.01
            particle.pos.y += dy * 0.01
            
            glColor3f(particle.color[0] / 255.0, particle.color[1] / 255.0, particle.color[2] / 255.0)
            glVertex2f(particle.pos.x, particle.pos.y)

            if abs(dx) > 0.1 or abs(dy) > 0.1:
                cont+=1
        
        glEnd()
        
        if cont <= len(self.particles_from_collision) * 0.84:
            self.restart_status = True
            # Remove 30% das partículas aleatoriamente
            num_to_remove = int(len(self.particles_from_collision) * 0.30)
            particles_to_remove = random.sample(self.particles_from_collision, num_to_remove)
            for particle in particles_to_remove:
                self.particles_from_collision.remove(particle)

            for particle in self.particles_from_collision:
                particle.noise_offset_x = random.uniform(0, 1000)
                particle.noise_offset_y = random.uniform(0, 1000)
                particle.speed = random.uniform(1, 3)
                
                # Vetor de direção com base na distância do centro
                particle.center_x, particle.center_y = self.WIDTH / 2, self.HEIGHT / 2
                direction_angle = math.atan2(particle.pos.y - particle.center_y, particle.pos.x - particle.center_x)
                particle.direction_x = math.cos(direction_angle)
                particle.direction_y = math.sin(direction_angle)

    def generate_points(self):
        experiment = doubleSlit()
        experiment.distance_to_screen = 10
        experiment.slit_dist = 3 
        experiment.clear_screen()
        if self.use_image:
            self.number_of_particles = len(self.images)
        experiment.electron_beam(num_electrons=self.number_of_particles)
        return experiment.get_positions()

    def transformar_pontos(self, pontos_x, pontos_y, x_min, x_max, y_min, y_max, screen_width, screen_height):
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

    def add_particle(self, position, direction, speed, radius, color_or_image, use_image):
        self.particles.append(Particle(position, direction, speed, radius, color_or_image, use_image))

    def set_particles_speed(self, speed):
        for particle in self.particles:
            particle.speed = speed

    def send_sound_params(self, peak_width_1_target, peak_width_2_target, bands_target, factor):
        self.osc_client.send_message("peak_width_1", int(self.peak_width_1))
        self.osc_client.send_message("peak_width_2", int(self.peak_width_2))
        self.osc_client.send_message("bands", int(self.bands))
        
        self.peak_width_1 += (peak_width_1_target - self.peak_width_1) * factor
        self.peak_width_2 += (peak_width_2_target - self.peak_width_2) * factor
        self.bands += (bands_target - self.bands) * factor

    def draw_particles_final_image(self):
        self.move_particles()
        self.send_sound_params(1024, 1024, 532, 0.01)
        # self.text_animation.draw_and_update()

    def draw_generated_particles(self, index_next_to_alive):
        glBegin(GL_POINTS)
            
        for i in range(index_next_to_alive):
            particle = self.particles_from_collision[i]
            particle.update_pos()
            glColor3f(particle.color[0] / 255.0, particle.color[1] / 255.0, particle.color[2] / 255.0)
            glVertex2f(particle.pos.x, particle.pos.y)
        
        glEnd()

    def create_generated_particles(self, result):
        self.to_alive_created_particle(result)
        x = random.uniform(result.pos.x - 20.0, result.pos.x + 20.0)
        y = random.uniform(result.pos.y - 20.0, result.pos.y + 20.0)
        self.to_alive_created_particle(Particle((x,y), result.dir, 1, 1, (0,0,0), False, False))
        x = random.uniform(result.pos.x - 40.0, result.pos.x + 40.0)
        y = random.uniform(result.pos.y - 40.0, result.pos.y + 40.0)
        self.to_alive_created_particle(Particle((x,y), result.dir, 1, 1, (0,0,0), False, False))
        x = random.uniform(result.pos.x - 80.0, result.pos.x + 80.0)
        y = random.uniform(result.pos.y - 80.0, result.pos.y + 80.0)
        self.to_alive_created_particle(Particle((x,y), result.dir, 1, 1, (0,0,0), False, False))
        self.to_alive_created_particle(result)

    def to_alive_created_particle(self, result):
        if self.index_next_to_alive < len(self.particles_from_collision):
            self.particles_from_collision[self.index_next_to_alive].pos = result.pos
            self.particles_from_collision[self.index_next_to_alive].dir = result.dir
            self.particles_from_collision[self.index_next_to_alive].speed = result.speed
            self.particles_from_collision[self.index_next_to_alive].radius = result.radius
            self.particles_from_collision[self.index_next_to_alive].alive = True
            self.index_next_to_alive += 1
        else:
            self.move_particle_status = True
            self.use_collision = False

    def draw_particles(self):

        if self.restart_status:
            self.move_particles_restart()
            return
        
        if self.move_particle_status:
            self.draw_particles_final_image()
            return
        
        self.particles_manager.clear_grid()

        self.draw_generated_particles(self.index_next_to_alive)

        for particle in self.particles:
            if self.wave_movement:
                update_wave_movement(self.timer, particle)
            else:
                particle.update_pos()
            # particle.draw()
            self.particles_manager.add_particle_to_grid(particle)
            i, j = self.particles_manager.get_particle_position_on_grid(particle)
            result = particle.guidance(self.box, self.particles_manager.grid[i][j], self.use_collision if self.face_detector.face_detected else False)
            if result != None and not self.move_particle_status:
                self.create_generated_particles(result)
        
        # self.timer += self.clock.get_time()
        current_time = time.time()
        delta_time = current_time - self.clock
        self.clock = current_time

        # Atualize o temporizador das partículas
        self.timer += delta_time

        if self.use_collision and self.face_detector.face_detected:
            self.time_transition_to_final_image_counter += self.timer//1000

        if self.time_transition_to_final_image_counter > self.time_transition_to_final_image: # esse trecho limita a geração de partículas a um tempo "time_transition_to_final_image". se passar disso, cria todas as partículas que faltam 
            qt = (int) ((len(self.particles_from_collision) - self.index_next_to_alive) // 2)
            for i in range(qt):
                particle = random.choice(self.particles)
                x = particle.pos.x
                y = particle.pos.y
                self.to_alive_created_particle(Particle((x,y), particle.dir, 1, 1, (0,0,0), False, False))

    def create_particles(self):
        for _ in range(self.number_of_particles):
            self.create_particle()

    def create_particle(self):
        if len(self.particles) < self.number_of_particles:
            pos = self.points[len(self.particles)]
            angle = random.uniform(0, 2 * math.pi)  
            dir = Vector2(math.cos(angle), math.sin(angle)).normalize()
            speed = self.particles_speed if self.face_detector.face_detected else 0
            radius = self.particles_radius
            if self.use_image:
                self.add_particle(pos, dir, speed, radius, self.images[len(self.particles)], use_image=True)
            else:
                self.add_particle(pos, dir, speed, radius, (255, 255, 255), use_image=False)

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpar a tela

        if not self.face_detector.face_detected:
            self.face_detector.face_detected = self.face_detector.process_face_detection()
            if self.face_detector.face_detected:
                self.set_particles_speed(self.particles_speed)
            else:
                self.set_particles_speed(0)

        if len(self.particles) < self.number_of_particles:
            self.create_particle()
            self.create_particle()
            self.create_particle()
        else:
            self.wave_movement = not self.face_detector.face_detected

        self.draw_particles()

        glutSwapBuffers()  # Trocar buffers

    def keyboard_event(key, x, y):
        if key == b'\x1b':  # Escape key
            sys.exit()

    def run(self):
        glutDisplayFunc(self.render)
        glutIdleFunc(self.render)
        glutKeyboardFunc(self.keyboard_event)
        glutMainLoop()

if __name__ == "__main__":
    simulation = ParticleSimulation()
    simulation.run()