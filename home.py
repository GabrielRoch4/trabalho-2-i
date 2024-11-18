import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Cores
BLUE = (0, 0, 153)
YELLOW = (239, 174, 84)
GREEN = (0, 128, 0)
RED = (255, 99, 71)
WHITE = (255, 255, 255)

# Dimensões da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect4 da Dani")

# Fonte (Usando a fonte baixada)
font_title = pygame.font.Font("Galindo-Regular.ttf", 80)
font_label = pygame.font.Font("Galindo-Regular.ttf", 25)
font_option = pygame.font.Font("Galindo-Regular.ttf", 23)
font_button = pygame.font.Font("Galindo-Regular.ttf", 30)

# Variáveis
clock = pygame.time.Clock()
ball_offset = 0
ball_direction = 1
input_active = False
input_text = ""
selected_algorithm = "Mini-max"
selected_ply = "1"

# Retângulos para seleção
algorithm_options = ["Mini-max", "Alfa-beta"]
ply_options = ["1", "2", "3", "4"]
algorithm_rects = []
ply_rects = []

# Configurações de animação
ball_speed = 2


def draw_title():
    """Desenha o título com bolinhas animadas."""
    title_surface = font_title.render("Connect4 da Dani", True, YELLOW)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, 80))
    screen.blit(title_surface, title_rect)

    # Animação de bolinhas
    global ball_offset, ball_direction
    if ball_offset >= 10 or ball_offset <= -10:
        ball_direction *= -1
    ball_offset += ball_speed * ball_direction

def draw_input_field():
    """Desenha o campo para nome do jogador."""
    label = font_label.render("Insira seu nome:", True, YELLOW)
    screen.blit(label, (WIDTH // 2 - 130, 150))

    input_rect = pygame.Rect((WIDTH // 2 - 150, 190), (300, 40))
    pygame.draw.rect(screen, WHITE if input_active else YELLOW, input_rect, 2)
    input_surface = font_option.render(input_text or "Seu nome", True, WHITE)
    screen.blit(input_surface, (input_rect.x + 10, input_rect.y + 5))


def draw_algorithm_options():
    """Desenha as opções de algoritmo."""
    label = font_label.render("Algoritmo:", True, YELLOW)
    screen.blit(label, (WIDTH // 2 - 150, 250))

    x, y = WIDTH // 2 - 150, 290
    for option in algorithm_options:
        rect = pygame.Rect((x, y), (140, 40))
        color = YELLOW if option == selected_algorithm else WHITE
        pygame.draw.rect(screen, color, rect, border_radius=5)
        text_surface = font_option.render(option, True, BLUE)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
        algorithm_rects.append((rect, option))
        x += 160  # Espaçamento horizontal


def draw_ply_options():
    """Desenha as opções de profundidade."""
    label = font_label.render("Ply:", True, YELLOW)
    screen.blit(label, (WIDTH // 2 - 150, 350))

    x, y = WIDTH // 2 - 150, 390
    for option in ply_options:
        rect = pygame.Rect((x, y), (60, 40))
        color = YELLOW if option == selected_ply else WHITE
        pygame.draw.rect(screen, color, rect, border_radius=5)
        text_surface = font_option.render(option, True, BLUE)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
        ply_rects.append((rect, option))
        x += 80  # Espaçamento horizontal


def draw_play_button():
    """Desenha o botão de jogar."""
    play_rect = pygame.Rect((WIDTH // 2 - 100, 470), (200, 50))
    pygame.draw.rect(screen, YELLOW, play_rect, border_radius=5)
    play_text = font_button.render("Jogar", True, BLUE)
    play_text_rect = play_text.get_rect(center=play_rect.center)
    screen.blit(play_text, play_text_rect)
    return play_rect


# Loop principal
running = True
while running:
    screen.fill(BLUE)
    algorithm_rects = []
    ply_rects = []

    # Desenha os elementos na tela
    draw_title()
    draw_input_field()
    draw_algorithm_options()
    draw_ply_options()
    play_button = draw_play_button()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Detectar clique na caixa de texto
            input_rect = pygame.Rect((WIDTH // 2 - 150, 190), (300, 40))
            input_active = input_rect.collidepoint(event.pos)

            # Detectar clique nas opções de algoritmo
            for rect, option in algorithm_rects:
                if rect.collidepoint(event.pos):
                    selected_algorithm = option

            # Detectar clique nas opções de profundidade
            for rect, option in ply_rects:
                if rect.collidepoint(event.pos):
                    selected_ply = option

            # Detectar clique no botão de jogar
            if play_button.collidepoint(event.pos):
                print(f"Nome: {input_text}")
                print(f"Algoritmo: {selected_algorithm}")
                print(f"Ply: {selected_ply}")

        if event.type == pygame.KEYDOWN and input_active:
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
