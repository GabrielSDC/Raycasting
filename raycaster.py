import pygame
import math

pygame.init()

size    = width, height = 600, 400
screen  = pygame.display.set_mode(size)
clock   = pygame.time.Clock()
running = True
dt      = 0
player  = pygame.Vector3(width / 2 + 4, height / 2 + 4, 0)
block   = 70
pixel   = 10
font    = pygame.font.get_default_font()
wr_font = pygame.font.SysFont(font, 28, True, False)

black   = (  0,   0,   0)
white   = (255, 255, 255)
grey    = (127, 127, 127)
red     = (255,   0,   0)
blue    = (  0,   0, 255)
green   = (  0, 255,   0)
yellow  = (255, 255,   0)
lt_grey = (211, 211, 211)
dk_grey = (169, 169, 169)

map_w, map_h = 9, 9
maps = [
    1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 0, 1, 0, 0, 0, 0, 0, 1,
    1, 0, 1, 0, 0, 0, 0, 0, 1,
    1, 0, 1, 1, 0, 1, 0, 0, 1,
    1, 0, 0, 0, 0, 1, 0, 0, 1,
    1, 0, 0, 0, 0, 1, 1, 0, 1,
    1, 0, 0, 0, 0, 0, 0, 0, 1,
    1, 0, 1, 0, 0, 1, 0, 0, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1
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

def draw_square(x, y, color, size):
    points = [(x, y), (x + size, y), (x + size, y + size), (x, y + size)]
    pygame.draw.polygon(screen, color, points, 0)

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

def display_map_2D():
    for y in range(map_h):
        for x in range(map_w):
            color = white if maps[y * map_w + x] else black
            draw_square(x * pixel, y * pixel, color, pixel)

def display_player():
    x, y = (player.x / block) * pixel, (player.y / block) * pixel
    pygame.draw.circle(screen, red, (x, y), 2)
    vision = (x + cos(player.z) * 5, y + sin(player.z) * 5)
    pygame.draw.line(screen, red, (x, y), vision, 1) 

def draw_screen(column: int, distance: float, color: tuple) -> None:
    wall_height = (40 * width) / distance
    ceiling = (height - wall_height) / 2
    floor   = height - ceiling
    for h in range(0, height, 10):
        if h < ceiling:
            draw_square(column * 10, h, blue, 10)
        elif h > floor:
            draw_square(column * 10, h, green, 10)
        else:

            draw_square(column * 10, h, color, 10)

def display_rays():
    ix, iy = 0, 0
    x_offset, y_offset = 0, 0
    a_ray = player.z - 30
    if a_ray < 0:
        a_ray += 360

    for n in range(60):
        # horizontal calculation
        h_distance = 0
        hx_ray, hy_ray = player.x, player.y

        if a_ray > 180 and a_ray < 360: 
            # looking up
            iy = -(player.y % block) - 0.000001
            ix = -iy / -tan(a_ray)
            
            y_offset = -block
            x_offset = -y_offset / -tan(a_ray)
        elif a_ray > 0 and a_ray < 180: 
            # looking down
            iy = block - player.y % block
            ix = iy * -tan(a_ray + 90)
            
            y_offset = block
            x_offset = y_offset * -tan(a_ray + 90)
        else: 
            # looking straight forward or backwards
            iy = 0
            ix = block - (player.x % block) if a_ray == 0 else -(player.x % block)
            
            y_offset = 0
            x_offset = block * (-1 if a_ray == 180 else 1)

        hx_ray += ix
        hy_ray += iy
        h_distance += calc_distance((player.x, player.y), (hx_ray, hy_ray))
        dist_offset = calc_distance((hx_ray, hy_ray), (hx_ray + x_offset, hy_ray + y_offset))

        for i in range(map_w):
            mx, my = int(hx_ray // block), int(hy_ray // block)
            position = my * map_w + mx
            if position >= 0 and position < map_w * map_h and maps[position]:
                break
            else:
                hx_ray += x_offset
                hy_ray += y_offset
                h_distance += dist_offset

        h_ray = (hx_ray, hy_ray)

        # vertical calculation
        v_distance = 0
        vx_ray, vy_ray = player.x, player.y

        if a_ray > 90 and a_ray < 270:
            # looking left
            ix = -(player.x % block) - 0.000001
            iy = ix * tan(a_ray)

            x_offset = -block
            y_offset = x_offset * tan(a_ray)
        elif a_ray < 90 or a_ray > 270:
            # looking right
            ix = block - (player.x % block)
            iy = ix * tan(a_ray)

            x_offset = block
            y_offset = x_offset * tan(a_ray)
        else:
            # looking straight upwards or downwards
            ix = 0
            iy = block - (player.y % block) if a_ray == 90 else -(a_ray % block)

            x_offset = 0
            y_offset = block * (-1 if a_ray == 270 else 1)
            
        vx_ray += ix
        vy_ray += iy
        v_distance += calc_distance((player.x, player.y), (vx_ray, vy_ray))
        dist_offset = calc_distance((vx_ray, vy_ray), (vx_ray + x_offset, vy_ray + y_offset))

        for i in range(map_h):
            mx, my = int(vx_ray // block), int(vy_ray // block)
            position = my * map_w + mx
            if position >= 0 and position < map_w * map_h and maps[position]:
                break
            else:
                vx_ray += x_offset
                vy_ray += y_offset
                v_distance += dist_offset

        v_ray = (vx_ray, vy_ray)

        diff_angle = player.z - a_ray
        if diff_angle < 0:
            diff_angle += 360
        elif diff_angle >= 360:
            diff_angle -= 360

        if h_distance < v_distance:
            draw_screen(n, h_distance * cos(diff_angle), lt_grey)
        else:
            draw_screen(n, v_distance * cos(diff_angle), dk_grey)
            
        a_ray += 1
        if a_ray >= 360:
            a_ray -= 360


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    handle_keydown(pygame.key.get_pressed())

    display_rays()
    display_map_2D()
    display_player()

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()