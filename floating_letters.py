import pygame
import random
import string

class TextAnimation:

    def split_phrase(self, phrase, max_width, letter_size):
        words = phrase.split(' ')
        lines = []
        current_line = ""

        for word in words:
            if current_line:  # Se já houver texto na linha, adicione um espaço antes da palavra
                test_line = current_line + " " + word
            else:
                test_line = word

            if len(test_line) * letter_size > max_width:
                lines.append(current_line.strip())
                current_line = word
            else:
                current_line = test_line
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines

    def calculate_final_positions(self, lines, start_x, start_y, letter_size, line_height):
        self.positions = []
        y = start_y
        for line in lines:
            x = start_x - (len(line) * letter_size) // 2
            for char in line:
                if char.strip():  # Verifica se o caractere não é um espaço vazio
                    self.positions.append((char, (x, y)))
                x += letter_size
            y += line_height

    def calculate_start_x_position(self, phrase, text_position, letter_size):
        total_width = len(phrase) * letter_size
        return text_position[0] - (total_width // 2)

    def __init__(self, phrase, screen_width, screen_height, text_position):
        self.phrase = phrase
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.initial_font_size = 2
        self.final_font_size = 20
        self.growth_duration = 300
        self.animation_velocity = 0.025
        self.letter_size_px = self.final_font_size // 2
        self.line_height_px = self.final_font_size
        max_width = screen_width // 2

        lines = self.split_phrase(phrase, max_width, self.letter_size_px)
        self.calculate_final_positions(lines, text_position[0], text_position[1], self.letter_size_px, self.line_height_px)

        # Verifica se a posição está vazia e se o caractere é válido antes de criar o GrowingLetter
        self.letters = [GrowingLetter(letter, pos, self.initial_font_size, self.final_font_size, self.growth_duration, self.screen_width, self.screen_height) 
                        for letter, pos in self.positions if letter.strip()]

    def draw_and_update(self, screen):
        for letter in self.letters:
            letter.update(self.animation_velocity)
            screen.blit(letter.image, letter.rect)

class GrowingLetter:
    def __init__(self, letter, final_position, initial_font_size, final_font_size, growth_duration, screen_width, screen_height):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.letter = letter
        self.final_x, self.final_y = final_position
        self.initial_font_size = initial_font_size
        self.final_font_size = final_font_size
        self.font_size = initial_font_size
        self.font = pygame.font.SysFont('arial', self.font_size)
        self.image = self.font.render(self.letter, True, (255, 255, 255))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.growth_counter = 0
        self.growth_duration = growth_duration

    def update(self, move_factor):
        if self.growth_counter < self.growth_duration:
            self.font_size = self.initial_font_size + (self.final_font_size - self.initial_font_size) * (self.growth_counter / self.growth_duration)
            self.font = pygame.font.SysFont('arial', int(self.font_size))
            self.image = self.font.render(self.letter, True, (255, 255, 255))
            self.rect = self.image.get_rect(center=(self.x, self.y))
            self.growth_counter += 1

        self.x = self.x + (self.final_x - self.x) * move_factor
        self.y = self.y + (self.final_y - self.y) * move_factor
        self.rect = self.image.get_rect(center=(self.x, self.y))


# # Inicialização do Pygame e da animação
# pygame.init()
# screen_width = 800
# screen_height = 600
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("Text Animation")
# clock = pygame.time.Clock()

# phrase = "Are some technical objects just in the background, while the closer one gets to an epistemic situation, the more attention needs to be paid to the technical objects that are implied"
# text_position = (screen_width // 2, screen_height // 2)
# animation = TextAnimation(phrase, screen_width, screen_height, text_position)

# # Loop principal
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
    
#     screen.fill((0, 0, 0))
#     animation.draw_and_update(screen)
#     pygame.display.flip()
#     clock.tick(30)

# pygame.quit()
