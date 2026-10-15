import random
import pygame

pygame.init()

# ==============================
# GAME SETTINGS
# ==============================

# Get your screen resolution
pygame.display.init()

info = pygame.display.Info()

# Set game window to 2/3 of screen size
WIDTH = int(info.current_w * 2 / 3)
HEIGHT = int(info.current_h * 2 / 3)

# Keep the game grid proportional to the window
CELL_SIZE = 20

GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Difficulty settings
DIFFICULTIES = {
    "Noob": 3,
    "Easy": 7,
    "Medium": 10,
    "Hard": 15,
    "Pro": 21,
    "Extreme": 30,
    "Impossible": 47
}

# Colors
BLACK = (18, 18, 24)
GREEN = (70, 220, 100)
DARK_GREEN = (35, 150, 70)
RED = (240, 75, 75)
WHITE = (245, 245, 245)
GRAY = (160, 160, 175)
YELLOW = (255, 220, 70)
ORANGE = (255, 150, 50)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 36, bold=True)
medium_font = pygame.font.SysFont("arial", 27)
small_font = pygame.font.SysFont("arial", 20)


# ==============================
# DRAW TEXT
# ==============================

def draw_text(text, font, color, x, y):
    image = font.render(text, True, color)
    rect = image.get_rect(center=(x, y))
    screen.blit(image, rect)


# ==============================
# DIFFICULTY MENU
# ==============================

def difficulty_menu():

    difficulties = list(DIFFICULTIES.items())

    while True:

        screen.fill(BLACK)

        draw_text(
            "SNAKE GAME",
            font,
            GREEN,
            WIDTH // 2,
            65
        )

        draw_text(
            "SELECT DIFFICULTY",
            medium_font,
            WHITE,
            WIDTH // 2,
            115
        )

        for index, (name, fps) in enumerate(difficulties):

            y = 160 + index * 45

            if name == "Noob":
                color = GREEN
            elif name == "Easy":
                color = (120, 220, 120)
            elif name == "Medium":
                color = YELLOW
            elif name == "Hard":
                color = ORANGE
            elif name == "Pro":
                color = RED
            elif name == "Extreme":
                color = (255, 90, 90)
            else:
                color = (255, 40, 120)

            draw_text(
                f"{index + 1}. {name}",
                medium_font,
                color,
                WIDTH // 2,
                y
            )

        draw_text(
            "Press 1-7 to choose your difficulty",
            small_font,
            GRAY,
            WIDTH // 2,
            HEIGHT - 200
        )

# Developer watermark
          
        watermark_font = pygame.font.SysFont("arial", 16)

        draw_text(
            "Developed by K Hasan M",
            watermark_font,
            GRAY,
            WIDTH // 2,
            HEIGHT - 38
        )
# Contact information
        contact_font = pygame.font.SysFont("arial", 14)

        draw_text(
        "Contact: t.me/iamkhm7",
        contact_font,
        GRAY,
        WIDTH // 2,
        HEIGHT - 15
        )
        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:

                if pygame.K_1 <= event.key <= pygame.K_7:
                    index = event.key - pygame.K_1
                    return difficulties[index]

                if pygame.K_ESCAPE:
                    pygame.quit()
                    raise SystemExit


# ==============================
# FOOD GENERATOR
# ==============================

def random_food(snake):

    empty_cells = [
        (x, y)
        for x in range(GRID_WIDTH)
        for y in range(GRID_HEIGHT)
        if (x, y) not in snake
    ]

    if empty_cells:
        return random.choice(empty_cells)

    return None


# ==============================
# DRAW CELL
# ==============================

def draw_cell(color, position):

    x, y = position

    rect = pygame.Rect(
        x * CELL_SIZE,
        y * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )

    pygame.draw.rect(
        screen,
        color,
        rect.inflate(-2, -2),
        border_radius=4
    )


# ==============================
# GAME OVER SCREEN
# ==============================

def game_over_screen(score, won):

    while True:

        screen.fill(BLACK)

        if won:
            draw_text(
                "YOU WIN!",
                font,
                GREEN,
                WIDTH // 2,
                HEIGHT // 2 - 80
            )
        else:
            draw_text(
                "GAME OVER",
                font,
                RED,
                WIDTH // 2,
                HEIGHT // 2 - 80
            )

        draw_text(
            f"Final Score: {score}",
            medium_font,
            WHITE,
            WIDTH // 2,
            HEIGHT // 2 - 25
        )

        draw_text(
            "ENTER - Play Again",
            small_font,
            YELLOW,
            WIDTH // 2,
            HEIGHT // 2 + 25
        )

        draw_text(
            "M - Main Menu",
            small_font,
            WHITE,
            WIDTH // 2,
            HEIGHT // 2 + 60
        )

        draw_text(
            "ESC - Quit",
            small_font,
            GRAY,
            WIDTH // 2,
            HEIGHT // 2 + 95
        )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    return "restart"

                if event.key == pygame.K_m:
                    return "menu"

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    raise SystemExit


# ==============================
# MAIN GAME
# ==============================

def play_game(difficulty, fps):

    snake = [
        (GRID_WIDTH // 2, GRID_HEIGHT // 2),
        (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
        (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)
    ]

    direction = (1, 0)
    next_direction = direction

    food = random_food(snake)

    score = 0
    game_over = False
    won = False

    while not game_over:

        # --------------------------
        # EVENTS
        # --------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return "menu"

                # Prevent reversing directly into yourself.
                if (
                    event.key in (pygame.K_UP, pygame.K_w)
                    and direction != (0, 1)
                ):
                    next_direction = (0, -1)

                elif (
                    event.key in (pygame.K_DOWN, pygame.K_s)
                    and direction != (0, -1)
                ):
                    next_direction = (0, 1)

                elif (
                    event.key in (pygame.K_LEFT, pygame.K_a)
                    and direction != (1, 0)
                ):
                    next_direction = (-1, 0)

                elif (
                    event.key in (pygame.K_RIGHT, pygame.K_d)
                    and direction != (-1, 0)
                ):
                    next_direction = (1, 0)

        # --------------------------
        # MOVE SNAKE
        # --------------------------

        direction = next_direction

        head_x, head_y = snake[0]
        dx, dy = direction

        new_head = (
            head_x + dx,
            head_y + dy
        )

        eating_food = new_head == food

        # Wall collision
        hit_wall = (
            new_head[0] < 0
            or new_head[0] >= GRID_WIDTH
            or new_head[1] < 0
            or new_head[1] >= GRID_HEIGHT
        )

        # Body collision
        body_to_check = snake if eating_food else snake[:-1]
        hit_self = new_head in body_to_check

        if hit_wall or hit_self:

            game_over = True

        else:

            snake.insert(0, new_head)

            if eating_food:

                score += 1
                food = random_food(snake)

                if food is None:
                    won = True
                    game_over = True

            else:

                snake.pop()

        # --------------------------
        # DRAW GAME
        # --------------------------

        screen.fill(BLACK)

        # Grid
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(
                screen,
                (28, 28, 36),
                (x, 0),
                (x, HEIGHT)
            )

        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(
                screen,
                (28, 28, 36),
                (0, y),
                (WIDTH, y)
            )

        # Food
        if food is not None:
            draw_cell(RED, food)

        # Snake
        for index, part in enumerate(snake):

            if index == 0:
                draw_cell(GREEN, part)
            else:
                draw_cell(DARK_GREEN, part)

        # Score
        score_image = small_font.render(
            f"Score: {score}",
            True,
            WHITE
        )

        screen.blit(score_image, (10, 8))

        # Difficulty
        info_image = small_font.render(
            difficulty,
            True,
            YELLOW
        )

        screen.blit(
            info_image,
            (WIDTH - info_image.get_width() - 10, 8)
        )

        pygame.display.flip()

        # Control speed
        clock.tick(fps)

    # --------------------------
    # GAME OVER ACTIONS
    # --------------------------

    return game_over_screen(score, won)


# ==============================
# MAIN PROGRAM
# ==============================

def main():

    while True:

        # Select difficulty
        difficulty, fps = difficulty_menu()

        # Start game
        while True:

            result = play_game(difficulty, fps)

            if result == "restart":
                continue

            if result == "menu":
                break


if __name__ == "__main__":
    main()