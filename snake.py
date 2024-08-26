import pygame
import random
import math

# Inisialisasi Pygame
pygame.init()

# Warna
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (200, 200, 255)

# Ukuran layar
WIDTH = 800
HEIGHT = 600

# Ukuran sel
CELL_SIZE = 20

# Kecepatan ular
SPEED = 10

# Inisialisasi layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Font
font = pygame.font.Font(None, 36)

# Fungsi untuk menggambar latar belakang
def draw_background():
    screen.fill(LIGHT_BLUE)
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLUE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLUE, (0, y), (WIDTH, y))

# Fungsi untuk menggambar makanan
def draw_food(food):
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, WHITE, (food[0] + 4, food[1] + 4, CELL_SIZE - 8, CELL_SIZE - 8))
    pygame.draw.rect(screen, RED, (food[0] + 8, food[1] + 8, CELL_SIZE - 16, CELL_SIZE - 16))

# Fungsi untuk menggambar ular
def draw_snake(snake):
    for i, segment in enumerate(snake):
        color = (0, max(255 - i * 5, 100), 0)
        pygame.draw.rect(screen, color, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, BLACK, (segment[0], segment[1], CELL_SIZE, CELL_SIZE), 1)
    
    # Gambar mata ular
    eye_color = (255, 255, 255)
    pupil_color = (0, 0, 0)
    eye_size = CELL_SIZE // 3
    pygame.draw.circle(screen, eye_color, (snake[0][0] + CELL_SIZE // 4, snake[0][1] + CELL_SIZE // 4), eye_size)
    pygame.draw.circle(screen, eye_color, (snake[0][0] + 3 * CELL_SIZE // 4, snake[0][1] + CELL_SIZE // 4), eye_size)
    pygame.draw.circle(screen, pupil_color, (snake[0][0] + CELL_SIZE // 4, snake[0][1] + CELL_SIZE // 4), eye_size // 2)
    pygame.draw.circle(screen, pupil_color, (snake[0][0] + 3 * CELL_SIZE // 4, snake[0][1] + CELL_SIZE // 4), eye_size // 2)

# Fungsi untuk menampilkan pesan game over
def show_game_over(score):
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart or Q to Quit", True, BLUE)
    
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
    
    pygame.display.flip()

# Fungsi utama permainan
def game():
    snake = [(WIDTH // 2, HEIGHT // 2)]
    snake_direction = (CELL_SIZE, 0)
    food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
            random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
    score = 0
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != (0, CELL_SIZE):
                    snake_direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and snake_direction != (0, -CELL_SIZE):
                    snake_direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and snake_direction != (CELL_SIZE, 0):
                    snake_direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake_direction != (-CELL_SIZE, 0):
                    snake_direction = (CELL_SIZE, 0)

        new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
        snake.insert(0, new_head)

        if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
            snake[0][1] < 0 or snake[0][1] >= HEIGHT):
            return show_game_over_screen(score)

        if snake[0] in snake[1:]:
            return show_game_over_screen(score)

        if snake[0] == food:
            score += 1
            food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                    random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
        else:
            snake.pop()

        draw_background()
        draw_snake(snake)
        draw_food(food)

        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(SPEED)

def show_game_over_screen(score):
    show_game_over(score)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    return False
    return False

def main():
    while True:
        if not game():
            break

main()
pygame.quit()
