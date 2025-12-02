import pygame
import random
import sys
import os
import time

pygame.init()

# --- FULLSCREEN CONFIGURATION ---
FULLSCREEN = True
GRID_SIZE = 40

info = pygame.display.Info()
if FULLSCREEN:
    WIDTH, HEIGHT = info.current_w, info.current_h
else:
    WIDTH, HEIGHT = 1200, 800

GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN if FULLSCREEN else 0)
pygame.display.set_caption("Snake Game V7 - INVINCIBLE GHOST MODE")

clock = pygame.time.Clock()
snake_speed = 10

GAME_STATE = "MENU"

script_dir = os.path.dirname(os.path.abspath(__file__))
image_folder = os.path.join(script_dir, "Images")

background = pygame.image.load(os.path.join(image_folder, "bluesky.png"))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

apple_img = pygame.image.load(os.path.join(image_folder, "apple.png"))
berry_img = pygame.image.load(os.path.join(image_folder, "berry.png"))

# Create golden fruit if image doesn't exist
try:
    golden_img = pygame.image.load(os.path.join(image_folder, "golden_fruit.png"))
except:
    golden_img = pygame.Surface((GRID_SIZE, GRID_SIZE))
    golden_img.fill((255, 215, 0))  # Gold color
    pygame.draw.circle(golden_img, (255, 255, 0), (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//3)

apple_img = pygame.transform.scale(apple_img, (GRID_SIZE, GRID_SIZE))
berry_img = pygame.transform.scale(berry_img, (GRID_SIZE, GRID_SIZE))
golden_img = pygame.transform.scale(golden_img, (GRID_SIZE, GRID_SIZE))

snake_color = (0, 255, 0)
snake_head_color = (0, 200, 0)
text_color = (255, 255, 255)
grid_color = (60, 60, 60)
black = (0, 0, 0)
white = (255, 255, 255)
gold = (255, 215, 0)

font_size = max(28, min(44, HEIGHT // 16))
large_font_size = max(64, min(96, HEIGHT // 8))
font = pygame.font.SysFont(None, font_size)
large_font = pygame.font.SysFont(None, large_font_size)

snake_pos = [5 * GRID_SIZE, 3 * GRID_SIZE]
snake_body = [[snake_pos[0], snake_pos[1]], [4 * GRID_SIZE, 3 * GRID_SIZE], [3 * GRID_SIZE, 3 * GRID_SIZE]]
direction = "RIGHT"
change_to = direction
score = 0

fruit_pos = [0, 0]
fruit_type = "apple"

# GHOST MODE variables
golden_fruit_pos = None
golden_fruit_duration = 0
ghost_mode_active = False
ghost_mode_end_time = 0

def spawn_fruit():
    global fruit_pos, fruit_type
    while True:
        new_pos = [
            random.randint(2, GRID_WIDTH - 3) * GRID_SIZE,
            random.randint(2, GRID_HEIGHT - 3) * GRID_SIZE
        ]
        if new_pos not in snake_body and new_pos != golden_fruit_pos:
            fruit_pos = new_pos
            fruit_type = random.choices(["apple", "berry"], weights=[3, 1])[0]
            break

def spawn_golden_fruit():
    global golden_fruit_pos, golden_fruit_duration
    if golden_fruit_pos is not None:
        return
    while True:
        new_pos = [
            random.randint(2, GRID_WIDTH - 3) * GRID_SIZE,
            random.randint(2, GRID_HEIGHT - 3) * GRID_SIZE
        ]
        if new_pos not in snake_body and new_pos != fruit_pos:
            golden_fruit_pos = new_pos
            golden_fruit_duration = time.time() + 15  # 15 seconds visibility
            break

def remove_golden_fruit():
    global golden_fruit_pos, golden_fruit_duration
    golden_fruit_pos = None
    golden_fruit_duration = 0

def activate_ghost_mode():
    global ghost_mode_active, ghost_mode_end_time
    ghost_mode_active = True
    ghost_mode_end_time = time.time() + 5  # 5 seconds ghost mode

def deactivate_ghost_mode():
    global ghost_mode_active
    ghost_mode_active = False

def reset_game():
    global snake_pos, snake_body, direction, change_to, score, ghost_mode_active
    snake_pos = [5 * GRID_SIZE, 3 * GRID_SIZE]
    snake_body = [[snake_pos[0], snake_pos[1]], [4 * GRID_SIZE, 3 * GRID_SIZE], [3 * GRID_SIZE, 3 * GRID_SIZE]]
    direction = "RIGHT"
    change_to = direction
    score = 0
    remove_golden_fruit()
    deactivate_ghost_mode()
    spawn_fruit()

def wrap_around_boundaries():
    """Wrap snake to opposite side during ghost mode"""
    global snake_pos
    if snake_pos[0] < 0:
        snake_pos[0] = WIDTH - GRID_SIZE
    elif snake_pos[0] >= WIDTH:
        snake_pos[0] = 0
    if snake_pos[1] < 0:
        snake_pos[1] = HEIGHT - GRID_SIZE
    elif snake_pos[1] >= HEIGHT:
        snake_pos[1] = 0

def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, grid_color, (x, 0), (x, HEIGHT), 2)
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, grid_color, (0, y), (WIDTH, y), 2)

def draw_snake_eyes():
    if len(snake_body) == 0:
        return
        
    head = snake_body[0]
    eye_radius = GRID_SIZE // 8
    eye_x_offset = GRID_SIZE // 4
    eye_y_offset = GRID_SIZE // 4
    
    if direction == "RIGHT":
        eye1_pos = (int(head[0] + eye_x_offset), int(head[1] + eye_y_offset))
        eye2_pos = (int(head[0] + eye_x_offset), int(head[1] + GRID_SIZE - eye_y_offset))
    elif direction == "LEFT":
        eye1_pos = (int(head[0] + GRID_SIZE - eye_x_offset), int(head[1] + eye_y_offset))
        eye2_pos = (int(head[0] + GRID_SIZE - eye_x_offset), int(head[1] + GRID_SIZE - eye_y_offset))
    elif direction == "UP":
        eye1_pos = (int(head[0] + eye_x_offset), int(head[1] + GRID_SIZE - eye_y_offset))
        eye2_pos = (int(head[0] + GRID_SIZE - eye_x_offset), int(head[1] + GRID_SIZE - eye_y_offset))
    else:  # DOWN
        eye1_pos = (int(head[0] + eye_x_offset), int(head[1] + eye_y_offset))
        eye2_pos = (int(head[0] + GRID_SIZE - eye_x_offset), int(head[1] + eye_y_offset))
    
    pygame.draw.circle(screen, white, eye1_pos, eye_radius + 2)
    pygame.draw.circle(screen, white, eye2_pos, eye_radius + 2)
    pygame.draw.circle(screen, black, eye1_pos, eye_radius)
    pygame.draw.circle(screen, black, eye2_pos, eye_radius)

def draw_menu():
    screen.blit(background, (0, 0))
    title = large_font.render("SNAKE GAME V7", True, text_color)
    subtitle = font.render("INVINCIBLE GHOST MODE", True, gold)
    start = font.render("ENTER=Start, ESC=Exit, F11=Toggle FS", True, text_color)
    screen.blit(title, title.get_rect(center=(WIDTH/2, HEIGHT/4)))
    screen.blit(subtitle, subtitle.get_rect(center=(WIDTH/2, HEIGHT/4 + 70)))
    screen.blit(start, start.get_rect(center=(WIDTH/2, HEIGHT/2)))
    pygame.display.update()

def draw_gameover():
    screen.blit(background, (0, 0))
    go = large_font.render("GAME OVER", True, (255, 0, 0))
    sc = font.render(f"Final Score: {score}", True, text_color)
    retry = font.render("SPACE=Menu, ESC=Exit, F11=Toggle FS", True, text_color)
    screen.blit(go, go.get_rect(center=(WIDTH/2, HEIGHT/3)))
    screen.blit(sc, sc.get_rect(center=(WIDTH/2, HEIGHT/3 + 80)))
    screen.blit(retry, retry.get_rect(center=(WIDTH/2, HEIGHT/3 + 140)))
    pygame.display.update()

def game_over_effect():
    flash = pygame.Surface((WIDTH, HEIGHT))
    flash.fill((255, 0, 0))
    flash.set_alpha(180)
    screen.blit(flash, (0, 0))
    pygame.display.update()
    pygame.time.delay(200)

def game_over():
    global GAME_STATE
    game_over_effect()
    GAME_STATE = "GAME_OVER"

def toggle_fullscreen():
    global screen, WIDTH, HEIGHT, GRID_WIDTH, GRID_HEIGHT, background, font, large_font
    info = pygame.display.Info()
    if screen.get_flags() & pygame.FULLSCREEN:
        WIDTH, HEIGHT = 1200, 800
    else:
        WIDTH, HEIGHT = info.current_w, info.current_h
    GRID_WIDTH = WIDTH // GRID_SIZE
    GRID_HEIGHT = HEIGHT // GRID_SIZE
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN if not (screen.get_flags() & pygame.FULLSCREEN) else 0)
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    apple_img = pygame.transform.scale(apple_img, (GRID_SIZE, GRID_SIZE))
    berry_img = pygame.transform.scale(berry_img, (GRID_SIZE, GRID_SIZE))
    golden_img = pygame.transform.scale(golden_img, (GRID_SIZE, GRID_SIZE))
    
    font_size = max(28, min(44, HEIGHT // 16))
    large_font_size = max(64, min(96, HEIGHT // 8))
    font = pygame.font.SysFont(None, font_size)
    large_font = pygame.font.SysFont(None, large_font_size)

reset_game()

# --- MAIN LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_F11:
                toggle_fullscreen()

            if GAME_STATE == "MENU":
                if event.key == pygame.K_RETURN:
                    reset_game()
                    GAME_STATE = "PLAYING"
            elif GAME_STATE == "GAME_OVER":
                if event.key == pygame.K_SPACE:
                    GAME_STATE = "MENU"
            elif GAME_STATE == "PLAYING":
                if event.key == pygame.K_RIGHT and direction != "LEFT":
                    change_to = "RIGHT"
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    change_to = "LEFT"
                if event.key == pygame.K_UP and direction != "DOWN":
                    change_to = "UP"
                if event.key == pygame.K_DOWN and direction != "UP":
                    change_to = "DOWN"

    if GAME_STATE == "MENU":
        draw_menu()
    elif GAME_STATE == "GAME_OVER":
        draw_gameover()
    elif GAME_STATE == "PLAYING":
        # Update direction and move
        direction = change_to
        if direction == "RIGHT":
            snake_pos[0] += GRID_SIZE
        elif direction == "LEFT":
            snake_pos[0] -= GRID_SIZE
        elif direction == "UP":
            snake_pos[1] -= GRID_SIZE
        elif direction == "DOWN":
            snake_pos[1] += GRID_SIZE

        # WRAP AROUND BOUNDARIES during ghost mode [web:30][web:31]
        if ghost_mode_active:
            wrap_around_boundaries()
        else:
            # Normal boundary check (game over if hit boundary)
            if snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT:
                game_over()
                continue

        snake_body.insert(0, list(snake_pos))

        # Eat normal fruit
        if snake_pos == fruit_pos:
            score += 1 if fruit_type == "apple" else 2
            spawn_fruit()
        else:
            snake_body.pop()

        # Eat golden fruit
        if golden_fruit_pos and snake_pos == golden_fruit_pos:
            activate_ghost_mode()
            remove_golden_fruit()

        # Golden fruit timeout
        if golden_fruit_pos and time.time() > golden_fruit_duration:
            remove_golden_fruit()

        # Random golden fruit spawn
        if not golden_fruit_pos and random.random() < 0.005:  # Reduced spawn rate
            spawn_golden_fruit()

        # Ghost mode timeout
        if ghost_mode_active and time.time() > ghost_mode_end_time:
            deactivate_ghost_mode()

        # Self collision ONLY when NOT in ghost mode
        if not ghost_mode_active and snake_pos in snake_body[1:]:
            game_over()
            continue

        # RENDERING
        screen.blit(background, (0, 0))
        draw_grid()

        # Draw fruits
        if fruit_type == "apple":
            screen.blit(apple_img, fruit_pos)
        elif fruit_type == "berry":
            screen.blit(berry_img, fruit_pos)

        if golden_fruit_pos:
            screen.blit(golden_img, golden_fruit_pos)

        # Draw snake body (transparent in ghost mode)
        for i, block in enumerate(snake_body[1:], 1):
            if ghost_mode_active:
                alpha = max(80, 200 - i * 8)
                surf = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
                surf.fill((255, 255, 255, alpha))
                screen.blit(surf, block)
            else:
                pygame.draw.rect(screen, snake_color, (*block, GRID_SIZE, GRID_SIZE))

        # Draw snake HEAD
        head_rect = (*snake_body[0], GRID_SIZE, GRID_SIZE)
        if ghost_mode_active:
            pygame.draw.rect(screen, gold, head_rect)
            pygame.draw.rect(screen, (255, 255, 0), head_rect, 4)
        else:
            pygame.draw.rect(screen, snake_head_color, head_rect)
            pygame.draw.rect(screen, black, head_rect, 3)
        
        draw_snake_eyes()

        # UI
        score_show = font.render(f"Score: {score}", True, text_color)
        screen.blit(score_show, (20, 20))

        if ghost_mode_active:
            remaining = max(0, ghost_mode_end_time - time.time())
            ghost_text = font.render(f"👻 GHOST MODE: {remaining:.1f}s", True, gold)
            screen.blit(ghost_text, (20, 60))

        pygame.display.update()
        clock.tick(snake_speed)
