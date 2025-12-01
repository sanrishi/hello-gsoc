import pygame
import random
import sys

pygame.init()

# Game window
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Snake Game - GSoC Journey")

# Snake settings
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
direction = "RIGHT"
change_to = direction

# Food
food_pos = [random.randrange(1, 60) * 10, random.randrange(1, 40) * 10]
food_spawn = True

clock = pygame.time.Clock()

# Text settings
font = pygame.font.SysFont("arial", 30)

def game_over():
    go_text = font.render("Game Over! Press R to Restart", True, (255, 0, 0))
    screen.blit(go_text, (120, 180))
    pygame.display.update()

    # Wait for restart
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return  # Restart the game loop

running = True
while True:  # Main loop for restart
    # Reset game state
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    direction = "RIGHT"
    change_to = direction
    food_pos = [random.randrange(1, 60) * 10, random.randrange(1, 40) * 10]
    food_spawn = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = "UP"
                if event.key == pygame.K_DOWN:
                    change_to = "DOWN"
                if event.key == pygame.K_LEFT:
                    change_to = "LEFT"
                if event.key == pygame.K_RIGHT:
                    change_to = "RIGHT"

        if change_to == "UP" and direction != "DOWN":
            direction = "UP"
        if change_to == "DOWN" and direction != "UP":
            direction = "DOWN"
        if change_to == "LEFT" and direction != "RIGHT":
            direction = "LEFT"
        if change_to == "RIGHT" and direction != "LEFT":
            direction = "RIGHT"

        if direction == "UP":
            snake_pos[1] -= 10
        if direction == "DOWN":
            snake_pos[1] += 10
        if direction == "LEFT":
            snake_pos[0] -= 10
        if direction == "RIGHT":
            snake_pos[0] += 10

        # Hit wall = Game Over
        if snake_pos[0] < 0 or snake_pos[0] > 590 or snake_pos[1] < 0 or snake_pos[1] > 390:
            game_over()
            break

        snake_body.insert(0, list(snake_pos))

        # Food collision
        if snake_pos == food_pos:
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, 60) * 10, random.randrange(1, 40) * 10]
            food_spawn = True

        # Self collision
        for block in snake_body[1:]:
            if snake_pos == block:
                game_over()
                break

        screen.fill((0,0,0))

        for block in snake_body:
            pygame.draw.rect(screen, (0,255,0), pygame.Rect(block[0], block[1], 10, 10))

        pygame.draw.rect(screen, (255,0,0), pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        pygame.display.update()
        clock.tick(15)
