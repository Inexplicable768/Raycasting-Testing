import pygame
from constants import Constants as C
from player import Player
import math
import numpy
import PIL.Image

# Constants
WIDTH, HEIGHT = 900, 700
FPS = 160  # FPS
FOV = 90  # Field of View
SENSITIVITY = math.pi / 256
MOVE_SPEED = 0.01
PRECISION = .02
WALL_COLOR = (229, 222, 222)
HUD_HEIGHT = 100
RES_X = 256
RES_Y = 256

# Initialize Pygame
pygame.init()
pygame.font.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Shooter Game - Python")
clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont('Comic Sans MS', 30)
previous_x, previous_y = pygame.mouse.get_pos()


# Load textures
wall_texture = pygame.image.load('src/Textures/bricks.png')
skybox_texture = pygame.image.load('src/Textures/skybox1.jpg')
enemy_texture = pygame.image.load('src/Textures/enemy.png')
texture_stone = pygame.image.load('src/Textures/stone.png')

# Map (map)
MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
]


# Player position and rotation
xpos, ypos = 1, 1
rotation = 0  # Rotation angle

wk, sk, ak, dk, SPACEk = False, False, False, False, False

def pause_menu():
    pass
def render_hud():
    current_fps = round(clock.get_fps(), 2)
    text_surface = font.render(f'FPS: {current_fps}', False, (0, 0, 0))
    Health_surface = font.render(f'Health: 100%', False, (0, 0, 0))

    display.blit(text_surface, (0,0))
def render_3d():
    texture_width, texture_height = wall_texture.get_size()  # Get the texture size

    for i in range(FOV + 11):
        ray_angle = rotation + math.radians(i - FOV / 2)
        x, y = xpos, ypos
        sin, cos = PRECISION * math.sin(ray_angle), PRECISION * math.cos(ray_angle)
        j = 0

        # Raycasting loop
        while True:
            x += cos
            y += sin
            j += 1
            if MAP[int(x)][int(y)] != 0:  # Hit a wall
                tile = MAP[int(x)][int(y)]
                distance = j
                j *= math.cos(math.radians(i - FOV / 2))
                height = (10 / j) * 2500
                break

        # Determine which wall was hit (horizontal or vertical)
        if abs(cos) > abs(sin):  # Vertical wall hit
            tex_x = int((x % 1) * texture_width)
        else:  # Horizontal wall hit
            tex_x = int((y % 1) * texture_height)





        # Calculate wall slice position
        top_of_wall = int((HEIGHT / 2) - height)
        bottom_of_wall = int((HEIGHT / 2) + height)
  # Draw the ceiling and floor
        pygame.draw.line(display, (0, 0, 255), (i * (WIDTH / FOV), 0), (i * (WIDTH / FOV), top_of_wall), width=int(WIDTH / FOV))
        pygame.draw.line(display, (20, 155, 0), (i * (WIDTH / FOV), bottom_of_wall), (i * (WIDTH / FOV), HEIGHT), width=int(WIDTH / FOV))


        # Scale the texture vertically
        texture_slice = wall_texture.subsurface((tex_x, 0, 1, texture_height))
        wall_height = bottom_of_wall - top_of_wall
        scaled_slice = pygame.transform.scale(texture_slice, (int(WIDTH / FOV), max(1, wall_height)))

        display.blit(scaled_slice, (i * (WIDTH / FOV), top_of_wall))



# Main game loop
while running:
    clock.tick(FPS)
    pygame.display.update()
    current_fps = clock.get_fps()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                wk = True
            elif event.key == pygame.K_s:
                sk = True
            elif event.key == pygame.K_a:
                ak = True
            elif event.key == pygame.K_d:
                dk = True
            elif event.key == pygame.K_SPACE:
                SPACEk = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                wk = False
            elif event.key == pygame.K_s:
                sk = False
            elif event.key == pygame.K_a:
                ak = False
            elif event.key == pygame.K_d:
                dk = False

    # Update player position and rotation
    x, y = xpos, ypos
    current_x, current_y = pygame.mouse.get_pos()

    if wk:
        x += MOVE_SPEED * math.cos(rotation)
        y += MOVE_SPEED * math.sin(rotation)
    if sk:
        x -= MOVE_SPEED * math.cos(rotation)
        y -= MOVE_SPEED * math.sin(rotation)
    if current_x != previous_x or current_y != previous_y:
        if current_x > previous_x:
            rotation += SENSITIVITY + .04
        if current_x < previous_x:
            rotation -= SENSITIVITY + .04
    previous_x, previous_y = current_x, current_y
    # Check for collision with MAP
    if MAP[int(x)][int(y)] == 0:
        xpos, ypos = x, y

    # Clear the display
    display.fill((0, 0, 0))
    render_3d()
    render_hud()

# Quit Pygame
pygame.quit()
