import pygame

pygame.init()

size    = width, height = 490, 490
screen  = pygame.display.set_mode(size)
clock   = pygame.time.Clock()
running = True
dt      = 0
player  = pygame.Vector2(width / 2 + 4, height / 2 + 4)
block   = 70
pixel   = 10

black = (0,     0,   0)
white = (255, 255, 255)
grey  = (127, 127, 127)
red   = (255,   0,   0)

maps = [
    1, 1, 1, 1, 1, 1, 1,
    1, 0, 1, 0, 0, 0, 1,
    1, 0, 1, 0, 0, 0, 1,
    1, 0, 1, 0, 0, 0, 1,
    1, 0, 0, 0, 1, 0, 1,
    1, 0, 0, 0, 0, 0, 1,
    1, 1, 1, 1, 1, 1, 1
]

def draw_square(x, y, color, size):
    points = [(x, y), (x + size, y), (x + size, y + size), (x, y + size)]
    pygame.draw.polygon(screen, color, points, 0)

def display_map():
    for y in range(0, height, block):
        i = y // block
        for x in range(0, width, block):
            j = x // block
            color = white if maps[i * 7 + j] else black
            draw_square(x + 1, y + 1, color, block - 2)

def handle_keydown(keys):
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.y -= block * dt + 1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.y += block * dt + 1
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= block * dt + 1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += block * dt + 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    handle_keydown(pygame.key.get_pressed())

    screen.fill(grey)

    display_map()
    draw_square(player.x, player.y, red, pixel)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()