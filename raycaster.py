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
font    = pygame.font.get_default_font()
wr_font = pygame.font.SysFont(font, 28, True, False)

black  = (  0,   0,   0)
white  = (255, 255, 255)
grey   = (127, 127, 127)
red    = (255,   0,   0)
green  = (  0,   0, 255)
yellow = (255, 255,   0)

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

def tan(deg: float) -> float:
    return math.tan(math.radians(deg))

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
        player.z += 360
    elif player.z >= 360:
        player.z -= 360

def display_player():
    pygame.draw.circle(screen, red, (player.x, player.y), pixel / 2)
    vision = (player.x + cos(player.z) * 20, player.y + sin(player.z) * 20)
    pygame.draw.line(screen, red, (player.x, player.y), vision, 2) 

def calc_distance(pos1: tuple, pos2: tuple) -> float:
    x1, y1 = pos1
    x2, y2 = pos2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def display_arrays():
    ix, iy = 0, 0
    x_offset, y_offset = 0, 0
    
    # horizontal calculation
    h_distance = 0
    x_ray, y_ray = player.x, player.y

    if player.z > 180 and player.z < 360: 
        # looking up
        iy = -(player.y % block) - 0.000001
        ix = -iy / -tan(player.z)
        
        y_offset = -block
        x_offset = -y_offset / -tan(player.z)
    elif player.z > 0 and player.z < 180: 
        # looking down
        iy = block - player.y % block
        ix = iy * -tan(player.z + 90)
        
        y_offset = block
        x_offset = y_offset * -tan(player.z + 90)
    else: 
        # looking straight forward or backwards
        iy = 0
        ix = block - (player.x % block) if player.z == 0 else -(player.x % block)
        
        y_offset = 0
        x_offset = block * (-1 if player.z == 180 else 1)

    x_ray += ix
    y_ray += iy
    h_distance += calc_distance((player.x, player.y), (x_ray, y_ray))
    dist_offset = calc_distance((x_ray, y_ray), (x_ray + x_offset, y_ray + y_offset))

    for i in range(7):
        mx, my = int(x_ray // block), int(y_ray // block)
        position = my * 7 + mx
        if position >= 0 and position < 49 and maps[position]:
            break
        else:
            x_ray += x_offset
            y_ray += y_offset
            h_distance += dist_offset

    h_ray = (x_ray, y_ray)

    # vertical calculation
    v_distance = 0
    x_ray, y_ray = player.x, player.y

    if player.z > 90 and player.z < 270:
        # looking left
        ix = -(player.x % block) - 0.000001
        iy = ix * tan(player.z)

        x_offset = -block
        y_offset = x_offset * tan(player.z)
    elif player.z < 90 or player.z > 270:
        # looking right
        ix = block - (player.x % block)
        iy = ix * tan(player.z)

        x_offset = block
        y_offset = x_offset * tan(player.z)
    else:
        # looking straight upwards or downwards
        ix = 0
        iy = block - (player.y % block) if player.z == 90 else -(player.z % block)

        x_offset = 0
        y_offset = block * (-1 if player.z == 270 else 1)
        
    x_ray += ix
    y_ray += iy
    v_distance += calc_distance((player.x, player.y), (x_ray, y_ray))
    dist_offset = calc_distance((x_ray, y_ray), (x_ray + x_offset, y_ray + y_offset))

    for i in range(7):
        mx, my = int(x_ray // block), int(y_ray // block)
        position = my * 7 + mx
        if position >= 0 and position < 49 and maps[position]:
            break
        else:
            x_ray += x_offset
            y_ray += y_offset
            v_distance += dist_offset

    v_ray = (x_ray, y_ray)

    if h_distance < v_distance:
        pygame.draw.line(screen, green, (player.x, player.y), h_ray, 3)
    else:
        pygame.draw.line(screen, green, (player.x, player.y), v_ray, 3)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    handle_keydown(pygame.key.get_pressed())

    screen.fill(grey)

    display_map()
    display_arrays()
    display_player()

    screen.blit(wr_font.render(f"{player.x:.1f}, {player.y:.1f}, {player.z:.1f}", True, black), (0, 0))

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()