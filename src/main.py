import pygame
import math
from constants import Constants as C

# Initialize Pygame
pygame.init()
pygame.font.init()
hud_font = pygame.font.Font("comicsans.ttf", 30)
screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load the texture for the wall
wall_texture = pygame.image.load('src/Textures/cobblestone.png')
skybox_texture = pygame.image.load('src/Textures/skybox1.jpg')

# Player class
class Player:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.health = 100
        self.armor = 100
        self.ammo = 60
        self.active = 0
        self.inventory = []

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self, da):
        self.angle += da

world_map = [
    "1111111111111111111111111111",
    "1000010000000000000000000001",
    "1000010000000000001000000001",
    "1000000000000000000000000001",
    "1000000000000000111000000001",
    "1000000000000000000000000001",
    "1000000000000000000000000001",
    "1000000000000000000000000001",
    "1111111111111111111111111111"
]

def cast_ray(player, angle):
    ray_x = player.x
    ray_y = player.y
    sin_a = math.sin(angle)
    cos_a = math.cos(angle)

    # Ray step increments
    step_size = 1

    for depth in range(C.MAX_DEPTH):
        ray_x += cos_a * step_size
        ray_y += sin_a * step_size

        map_x = int(ray_x // 64)
        map_y = int(ray_y // 64)

        if map_x < 0 or map_x >= len(world_map[0]) or map_y < 0 or map_y >= len(world_map):
            return C.MAX_DEPTH

        if world_map[map_y][map_x] == '1':
            return depth
    return C.MAX_DEPTH

def render_3d(player):
    for ray in range(C.NUM_RAYS):
        ray_angle = player.angle - C.HALF_FOV + (ray / C.NUM_RAYS) * C.FOV
        depth = cast_ray(player, ray_angle)

        if depth <= 0:
            depth = -depth + 1
        line_height = C.SCREEN_HEIGHT / (depth / 100)
        
        x_pos = ray * (C.SCREEN_WIDTH / C.NUM_RAYS)
        y_pos = (C.SCREEN_HEIGHT - line_height) / 2

        texture_width = wall_texture.get_width()
        texture_height = wall_texture.get_height()

        texture_offset = int(depth % texture_height)

        texture_section = wall_texture.subsurface(0, texture_offset, texture_width, texture_height - texture_offset)
        
        texture_section = pygame.transform.scale(texture_section, (C.SCREEN_WIDTH // C.NUM_RAYS, int(line_height)))

        screen.blit(texture_section, (x_pos, y_pos))

        floor_color = C.FLOOR_COLOR  
        floor_top = y_pos + line_height  
        pygame.draw.rect(screen, floor_color, (x_pos, floor_top, C.SCREEN_WIDTH // C.NUM_RAYS, C.SCREEN_HEIGHT - floor_top))

def render_hud(player):
    text_Health = hud_font.render('Health: ' + str(player.health) + "%", True, C.BLACK)
    text_Armor = hud_font.render('Armor: ' + str(player.armor) + "%", True, C.BLACK)

    screen.blit(text_Health, (10, 10))
    screen.blit(text_Armor, (200, 10))

def respawn():
    pass
def init():
    player = Player(100, 100, math.pi / 4)  # Starting position and angle
    running = True

    while running:
        #screen.fill(C.SKYBOX)
        bg = pygame.image.load("src/Textures/skybox1.jpg")
        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move(math.cos(player.angle) * C.MOVE_SPEED, math.sin(player.angle) * C.MOVE_SPEED)
        if keys[pygame.K_s]:
            player.move(-math.cos(player.angle) * C.MOVE_SPEED, -math.sin(player.angle) * C.MOVE_SPEED)
        if keys[pygame.K_LEFT]:
            player.rotate(-C.ROTATE_SPEED)
        if keys[pygame.K_RIGHT]:
            player.rotate(C.ROTATE_SPEED)

        # Raycasting and 3D rendering
        render_3d(player)
        render_hud(player)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    init()
