import pygame
import math

pygame.init()

size    = width, height = 600, 400
screen  = pygame.display.set_mode(size)
clock   = pygame.time.Clock()
running = True
dt      = 0
player  = pygame.Vector3(width / 2, height / 2, 0)
FOV     = 60
BLOCK   = 70
PIXEL   = 10
NUM_RAY = 120

# font    = pygame.font.get_default_font()
# wr_font = pygame.font.SysFont(font, 28, True, False)

black   = (  0,   0,   0)
white   = (255, 255, 255)
grey    = (127, 127, 127)
red     = (255,   0,   0)
blue    = (  0,   0, 255)
green   = (  0, 255,   0)
yellow  = (255, 255,   0)
lt_grey = (211, 211, 211)
dk_grey = (169, 169, 169)

map_w, map_h = 10, 10
maps = [
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 0, 0, 0, 0, 0, 1, 0, 0, 1,
    1, 0, 1, 0, 0, 0, 1, 0, 1, 1,
    1, 0, 1, 0, 0, 0, 0, 0, 0, 1,
    1, 0, 1, 1, 1, 1, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 1, 0, 1, 1, 1,
    1, 0, 0, 0, 0, 1, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
    1, 0, 1, 0, 0, 1, 0, 0, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1
]

def sin(deg: float) -> float:
    return math.sin(math.radians(deg))

def cos(deg: float) -> float:
    return math.cos(math.radians(deg))

def tan(deg: float) -> float:
    return math.tan(math.radians(deg))

def calc_distance(pos1: tuple, pos2: tuple) -> float:
    x1, y1 = pos1
    x2, y2 = pos2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def draw_square(x: float, y: float, color: tuple, size: float) -> None:
    points = [(x, y), (x + size, y), (x + size, y + size), (x, y + size)]
    pygame.draw.polygon(screen, color, points, 0)

def handle_keydown(keys: list[bool]) -> None:
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.x += cos(player.z) * BLOCK * dt
        player.y += sin(player.z) * BLOCK * dt
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.x -= cos(player.z) * BLOCK * dt
        player.y -= sin(player.z) * BLOCK * dt
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.z -= 90 * dt 
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.z += 90 * dt
    
    if player.z < 0:
        player.z += 360
    elif player.z >= 360:
        player.z -= 360

def draw_brackground() -> None:
    b = 255
    for i in range(0, int(height / 2), 10):
        pygame.draw.line(screen, (0, 0, b), (0, i), (width, i), 10)
        b -= 5

    g = 100
    for i in range(int(height / 2), int(height) + 1, 10):
        pygame.draw.line(screen, (0, g, 0), (0, i), (width, i), 10)
        g += 5

def display_mini_map() -> None:
    for y in range(map_h):
        for x in range(map_w):
            color = white if maps[y * map_w + x] else black
            draw_square(x * PIXEL, y * PIXEL, color, PIXEL)

    x, y = (player.x / BLOCK) * PIXEL, (player.y / BLOCK) * PIXEL
    pygame.draw.circle(screen, red, (x, y), 2)
    vision = (x + cos(player.z) * 5, y + sin(player.z) * 5)
    pygame.draw.line(screen, red, (x, y), vision, 1) 

def display_walls(column: int, distance: float, color: tuple, lwidth: float) -> None:
    wall_height = (40 * width) / distance
    ceiling = (height - wall_height) / 2
    floor = height - ceiling
    pygame.draw.line(screen, color, (column, ceiling), (column, floor), int(lwidth))

def cast_rays() -> None:
    ix, iy = 0, 0
    x_offset, y_offset = 0, 0
    a_ray = player.z - 30
    if a_ray < 0:
        a_ray += 360

    for n in range(NUM_RAY):
        # horizontal calculation
        h_distance = 0
        hx_ray, hy_ray = player.x, player.y

        if a_ray > 180 and a_ray < 360: 
            # looking up
            iy = -(player.y % BLOCK) - 0.000001
            ix = -iy / -tan(a_ray)
            
            y_offset = -BLOCK
            x_offset = -y_offset / -tan(a_ray)
        elif a_ray > 0 and a_ray < 180: 
            # looking down
            iy = BLOCK - player.y % BLOCK
            ix = iy * -tan(a_ray + 90)
            
            y_offset = BLOCK
            x_offset = y_offset * -tan(a_ray + 90)
        else: 
            # looking straight forward or backwards
            iy = 0
            ix = BLOCK - (player.x % BLOCK) if a_ray == 0 else -(player.x % BLOCK)
            
            y_offset = 0
            x_offset = BLOCK * (-1 if a_ray == 180 else 1)

        hx_ray += ix
        hy_ray += iy
        h_distance += calc_distance((player.x, player.y), (hx_ray, hy_ray))
        dist_offset = calc_distance((hx_ray, hy_ray), (hx_ray + x_offset, hy_ray + y_offset))

        for i in range(map_w):
            mx, my = int(hx_ray // BLOCK), int(hy_ray // BLOCK)
            position = my * map_w + mx
            if position >= 0 and position < map_w * map_h and maps[position]:
                break
            else:
                hx_ray += x_offset
                hy_ray += y_offset
                h_distance += dist_offset

        # vertical calculation
        v_distance = 0
        vx_ray, vy_ray = player.x, player.y

        if a_ray > 90 and a_ray < 270:
            # looking left
            ix = -(player.x % BLOCK) - 0.000001
            iy = ix * tan(a_ray)

            x_offset = -BLOCK
            y_offset = x_offset * tan(a_ray)
        elif a_ray < 90 or a_ray > 270:
            # looking right
            ix = BLOCK - (player.x % BLOCK)
            iy = ix * tan(a_ray)

            x_offset = BLOCK
            y_offset = x_offset * tan(a_ray)
        else:
            # looking straight upwards or downwards
            ix = 0
            iy = BLOCK - (player.y % BLOCK) if a_ray == 90 else -(a_ray % BLOCK)

            x_offset = 0
            y_offset = BLOCK * (-1 if a_ray == 270 else 1)
            
        vx_ray += ix
        vy_ray += iy
        v_distance += calc_distance((player.x, player.y), (vx_ray, vy_ray))
        dist_offset = calc_distance((vx_ray, vy_ray), (vx_ray + x_offset, vy_ray + y_offset))

        for i in range(map_h):
            mx, my = int(vx_ray // BLOCK), int(vy_ray // BLOCK)
            position = my * map_w + mx
            if position >= 0 and position < map_w * map_h and maps[position]:
                break
            else:
                vx_ray += x_offset
                vy_ray += y_offset
                v_distance += dist_offset

        diff_angle = player.z - a_ray
        if diff_angle < 0:
            diff_angle += 360
        elif diff_angle >= 360:
            diff_angle -= 360

        lwidth = width / NUM_RAY
        lpos = lwidth * (n + 1/2)
        if h_distance < v_distance:
            display_walls(lpos, h_distance * cos(diff_angle), lt_grey, lwidth)
        else:
            display_walls(lpos, v_distance * cos(diff_angle), dk_grey, lwidth)
            
        a_ray += FOV / NUM_RAY
        if a_ray >= 360:
            a_ray -= 360

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    handle_keydown(pygame.key.get_pressed())

    draw_brackground()
    cast_rays()
    display_mini_map()

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()