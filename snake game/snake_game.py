import pygame
import time
import random
import sys

pygame.init()

# Screen
WIDTH = 720
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game V2")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (160, 32, 240)
RED = (213, 50, 50)
BLUE = (30, 144, 255)

clock = pygame.time.Clock()
snake_block = 20
snake_speed = 12

font_style = pygame.font.SysFont("bahnschrift", 25)
menu_font = pygame.font.SysFont("consolas", 60)
info_font = pygame.font.SysFont("consolas", 28)

def message(msg, color, y):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [WIDTH / 6, y])

# Snake Drawing
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_block, snake_block])

# Score
def draw_score(score):
    val = font_style.render("Score: " + str(score), True, BLUE)
    screen.blit(val, [0, 0])

# Main Menu
def main_menu():
    selected = 0
    menu_items = ["START GAME", "QUIT"]

    title_y = 120
    title_direction = 1

    while True:
        screen.fill(BLACK)

        # Title Animation
        title = menu_font.render("SNAKE GAME", True, GREEN)
        screen.blit(title, (WIDTH/2 - title.get_width()/2, title_y))
        title_y += title_direction
        if title_y < 110 or title_y > 130:
            title_direction *= -1

        # Menu Options
        for i, text in enumerate(menu_items):
            color = WHITE if i == selected else (150, 150, 150)
            item = info_font.render(text, True, color)
            screen.blit(item, (WIDTH/2 - item.get_width()/2, 250 + i*50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected > 0:
                    selected -= 1
                elif event.key == pygame.K_DOWN and selected < len(menu_items)-1:
                    selected += 1
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        game_loop()
                    else:
                        pygame.quit()
                        sys.exit()

        clock.tick(10)

# Game Loop
def game_loop():
    game_over = False
    game_close = False

    x = WIDTH / 2
    y = HEIGHT / 2
    dx = 0
    dy = 0

    snake_list = []
    length = 1

    food_x = round(random.randrange(0, WIDTH - snake_block) / 20) * 20
    food_y = round(random.randrange(0, HEIGHT - snake_block) / 20) * 20

    # Berry
    berry_active = False
    berry_x = berry_y = 0

    score = 0

    while not game_over:

        while game_close:
            screen.fill(BLACK)
            message("Game Over! Press ENTER to restart", RED, HEIGHT/3)
            message("Press Q to Quit", RED, HEIGHT/2)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_RETURN:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -snake_block
                    dy = 0
                elif event.key == pygame.K_RIGHT:
                    dx = snake_block
                    dy = 0
                elif event.key == pygame.K_UP:
                    dy = -snake_block
                    dx = 0
                elif event.key == pygame.K_DOWN:
                    dy = snake_block
                    dx = 0

        x += dx
        y += dy

        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, [food_x, food_y, snake_block, snake_block])  # Food

        # Draw Berry if active
        if berry_active:
            pygame.draw.rect(screen, PURPLE, [berry_x, berry_y, snake_block, snake_block])

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > length:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(snake_block, snake_list)
        draw_score(score)

        pygame.display.update()

        # Eating food
        if x == food_x and y == food_y:
            score += 1
            length += 1
            food_x = round(random.randrange(0, WIDTH - snake_block) / 20) * 20
            food_y = round(random.randrange(0, HEIGHT - snake_block) / 20) * 20

            # Chance for berry to spawn (15%)
            if random.random() < 0.15:
                berry_active = True
                berry_x = round(random.randrange(0, WIDTH - snake_block) / 20) * 20
                berry_y = round(random.randrange(0, HEIGHT - snake_block) / 20) * 20

        # Eating berry
        if berry_active and x == berry_x and y == berry_y:
            score += 5
            length += 2
            berry_active = False

        clock.tick(snake_speed)

    pygame.quit()
    sys.exit()

main_menu()
