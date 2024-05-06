import pygame
import math

pygame.init()

size    = width, height = 490, 490
screen  = pygame.display.set_mode(size)
clock   = pygame.time.Clock()
running = True
dt      = 0
player  = pygame.Vector3(width / 2 + 4, height / 2 + 4, 0)
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

def sin(deg: float) -> float:
    return math.sin(math.radians(deg))

def cos(deg: float) -> float:
    return math.cos(math.radians(deg))

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
        player.x += cos(player.z) * block * dt
        player.y += sin(player.z) * block * dt
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.x -= cos(player.z) * block * dt
        player.y -= sin(player.z) * block * dt
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.z -= 90 * dt 
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.z += 90 * dt
    
    if player.z < 0:
        player.z = 359
    elif player.z > 360:
        player.z = 1

def display_player():
    pygame.draw.circle(screen, red, (player.x, player.y), pixel)
    vision = (player.x + cos(player.z) * 20, player.y + sin(player.z) * 20)
    pygame.draw.line(screen, red, (player.x, player.y), vision, 2) 

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    handle_keydown(pygame.key.get_pressed())

    screen.fill(grey)

    display_map()
    display_player()

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()