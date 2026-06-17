import pygame as pg
import random as rd
import sys

pg.init()



screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
WIDTH, HEIGHT = screen.get_width(), screen.get_height()
pg.display.set_caption("Colour Tap")

clock = pg.time.Clock()



small_font = pg.font.Font(None, 30)
medium_font = pg.font.Font(None, 50)
large_font = pg.font.Font(None, 80)



RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
WHITE = (245, 245, 245)
BLACK = (0, 0, 0)

safe_colours = [RED, GREEN, BLUE]



cols, rows = 6, 2
margin_x = WIDTH // (cols + 1)
margin_y = HEIGHT // 3

circles = [
    (margin_x * (c + 1), margin_y * (r + 1))
    for r in range(rows)
    for c in range(cols)
]

RADIUS = 52

# ======================
# GAME SETTINGS
# ======================

SPAWN_RATE = 900
PURPLE_RATE = 0.05



points = 0
miss_streak = 0   # tracks safe rounds missed

circle_colours = []
spawn_timer = pg.time.get_ticks()

def spawn_colors():
    global circle_colours
    circle_colours = [
        PURPLE if rd.random() < PURPLE_RATE else rd.choice(safe_colours)
        for _ in circles
    ]

spawn_colors()


def draw_start():
    screen.fill(WHITE)

    screen.blit(large_font.render("COLOUR TAP", True, BLACK), (WIDTH//2 - 160, 80))

    rules = [
        "SPACE when NO purple is visible",
        "Purple = instant loss",
        "Correct tap = +1 point",
        "Missing 3 safe rounds = -1 point"
    ]

    y = 220
    for line in rules:
        screen.blit(medium_font.render(line, True, BLACK), (140, y))
        y += 60

    screen.blit(
        large_font.render("PRESS ENTER TO START", True, BLACK),
        (WIDTH//2 - 320, HEIGHT - 120)
    )

    pg.display.update()



waiting = True
while waiting:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()

            if event.key == pg.K_RETURN:
                waiting = False

    draw_start()




running = True

while running:

    now = pg.time.get_ticks()

    if now - spawn_timer >= SPAWN_RATE:
        spawn_colors()
        spawn_timer = now

        # SAFE ROUND CHECK (no purple = missed opportunity)
        if PURPLE not in circle_colours:
            miss_streak += 1

            if miss_streak >= 3:
                points = max(0, points - 1)
                miss_streak = 0

        else:
            miss_streak = 0



    for event in pg.event.get():

        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:


            if event.key == pg.K_SPACE:

                if PURPLE in circle_colours:
                    running = False
                else:
                    points += 1



    screen.fill(WHITE)

    screen.blit(
        small_font.render(f"POINTS: {points}", True, BLACK),
        (20, 20)
    )

    screen.blit(
        small_font.render("SPACE to react", True, BLACK),
        (20, 60)
    )

    for i, (x, y) in enumerate(circles):
        pg.draw.circle(screen, circle_colours[i], (x, y), RADIUS)

    pg.display.update()
    clock.tick(60)




countdown_start = pg.time.get_ticks()
countdown = 3

while countdown > 0:

    now = pg.time.get_ticks()

    # update countdown every second
    new_count = 3 - ((now - countdown_start) // 1000)

    if new_count != countdown:
        countdown = new_count

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
            sys.exit()

    screen.fill(WHITE)

    screen.blit(
        large_font.render("GAME OVER", True, PURPLE),
        (WIDTH//2 - 170, 180)
    )

    screen.blit(
        medium_font.render(f"Points: {points}", True, BLACK),
        (WIDTH//2 - 120, 320)
    )
    screen.blit(
        large_font.render(f"Game closes in {countdown}", True, BLACK),
        (WIDTH//2 - 30, 450)
    )

    pg.display.update()
    clock.tick(60)

pg.quit()
sys.exit()
