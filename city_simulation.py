import pygame
import sys
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math

# Initialize Pygame
pygame.init()



# Screen dimensions
WIDTH, HEIGHT = 1200, 670
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Scene with Moving Car, Cloud, and Metro Rail")

# Day and night colors
DAY_SKY = (135, 206, 235)
NIGHT_SKY = (10, 10, 50)
DAY_SUN = (255, 255, 0)
NIGHT_MOON = (220, 220, 220)
DAY_BUILDING = (200, 214, 229)
NIGHT_BUILDING = (50, 50, 80)
DAY_WINDOW = (223, 249, 251)
NIGHT_WINDOW = (255, 255, 150)  # Lighted windows at night
DAY_GRASS = (29, 209, 161)
NIGHT_GRASS = (10, 80, 30)



#car

CAR_COLOR = (200, 50, 50)  # লাল গাড়ি
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_COLOR = (200, 230, 255)
ROAD_COLOR = (60, 60, 60)
GRASS_COLOR = (30, 120, 30)
SKY_COLOR = (135, 206, 235)
YELLOW = (255, 255, 0)



# Colors
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
SUN_YELLOW = (255, 255, 0)
BUILDING_COLOR = (255, 200, 200)
TREE_COLOR = (0, 128, 0)
ROAD_COLOR = (50, 50, 50)
LIGHT_COLOR = (255, 0, 0)
WINDOW_COLOR_OF_BILDING = (223, 249, 251)
ROAD_MIDLE = (236, 240, 241)
METRO_COLOR = (100, 100, 100)
METRO_TRACK_COLOR = (70, 70, 70)
METRO_WINDOW_COLOR = (200, 200, 255)
PILLAR_COLOR = (80, 80, 80)

FRONT_BUILDING_COLOR1 = (248, 239, 186)
FRONT_BUILDING_COLOR2 = (234, 181, 67)
FRONT_BUILDING_COLOR3 = (254, 164, 127)
TRUNK_BROWN = (101, 67, 33)
LEAF_GREEN = (50, 205, 50)

# Initial positions for moving elements
cloud_pos_x1 = -200
cloud_pos_x2 = -400
car1_pos_x = -100
car2_pos_x = 1300
metro_pos_x = -1000 

car3_pos_x = -200
car4_pos_x = 1300


#sate
is_day = True


# Metro rail track position (now in the middle)
TRACK_HEIGHT = 300  # Vertical position of the track

points = [
    (240, 420),  # Top-left
    (320, 420),  # Top-right
    (340, 450),  # Bottom-right
    (220, 450)   # Bottom-left
]



def draw_car(x, y,CAR_COLOR1,pos_hl,pos_driver):
    # গাড়ির বডি
    pygame.draw.rect(screen, CAR_COLOR1, (x-60, y-30, 120, 40))
    
    # গাড়ির ছাদ
    pygame.draw.rect(screen, CAR_COLOR1, (x-50, y-50, 100, 30))
    
    # জানালা
    pygame.draw.rect(screen, WINDOW_COLOR, (x-45, y-45, 40, 20))
    pygame.draw.rect(screen, WINDOW_COLOR, (x+5, y-45, 40, 20))
    
    # ড্রাইভার
    pygame.draw.circle(screen, (240, 200, 160), (x+pos_driver, y-35), 8)
    
    # চাকা
    pygame.draw.circle(screen, BLACK, (x-40, y+10), 15)
    pygame.draw.circle(screen, BLACK, (x+40, y+10), 15)
    

    # হেডলাইট
    headlight_color = WHITE if is_day else YELLOW
    pygame.draw.ellipse(screen, headlight_color, (x+pos_hl, y-25, 20, 10))
    pygame.draw.ellipse(screen, headlight_color, (x+pos_hl, y-5, 20, 10))



def draw_wavy_leaves(x, y, size):
    points = []
    # Create wavy pattern
    for angle in range(0, 360, 10):  # 10° steps
        rad = math.radians(angle)
        # Base circle with wavy modulation
        radius = size * (0.9 + 0.1 * math.sin(rad * 3))
        px = x + radius * math.cos(rad)
        py = y + radius * math.sin(rad)
        points.append((px, py))
    # pygame.draw.polygon(screen, LEAF_GREEN, points)
    leaf_color = LEAF_GREEN if is_day else (10, 60, 10)
    pygame.draw.polygon(screen, leaf_color, points)


def draw_dense_tree(x,y):
    # ট্রাঙ্ক
    trunk_width = 28
    trunk_height = 160
    tree_x = x
    tree_y = y
    
    # কাণ্ড
    pygame.draw.rect(screen, (101, 67, 33), 
                   (tree_x-trunk_width//2, tree_y-trunk_height, 
                    trunk_width, trunk_height))
    
    # ঘন patar (৩টি স্তর)
    colors = [
        (100, (34, 139, 34), (10, 50, 10)),
        (80, (50, 205, 50), (20, 70, 20)),
        (60, (144, 238, 144), (30, 90, 30))
    ]
    

    for i, (size, day_color, night_color) in enumerate(colors):
        color = day_color if is_day else night_color
        points = []
        for angle in range(0, 360, 10):
            rad = math.radians(angle)
            variation = 0.1 * math.sin(rad * (i+3))
            radius = size * (0.8 + variation)
            px = tree_x + radius * math.cos(rad)
            py = tree_y - trunk_height + (i*30) + radius * math.sin(rad)
            points.append((px, py))
        pygame.draw.polygon(screen, color, points)

def draw_pine_tree(x, y):
    # ট্রাঙ্ক
    trunk_width = 20
    trunk_height = 200
    tree_x = x
    tree_y = y
    
    # কাণ্ড
    pygame.draw.rect(screen, (74, 53, 27), 
                   (tree_x-trunk_width//2, tree_y-trunk_height, 
                    trunk_width, trunk_height))
    
    layers = [
        (120, 40, (34, 139, 34), (10, 50, 10)),
        (100, 60, (50, 205, 50), (20, 70, 20)),
        (80, 80, (60, 179, 113), (30, 90, 30)),
        (60, 100, (152, 251, 152), (40, 100, 40))
    ]
    
    for width, height, day_color, night_color in layers:
        color = day_color if is_day else night_color
        points = [
            (tree_x - width//2, tree_y - trunk_height + height),
            (tree_x, tree_y - trunk_height),
            (tree_x + width//2, tree_y - trunk_height + height)
        ]
        pygame.draw.polygon(screen, color, points)

def draw_tree(x,y):
    # Position and size
    trunk_width = 30
    trunk_height = 120
    tree_x = x
    tree_y = y

    pygame.draw.rect(screen, TRUNK_BROWN, 
                    (tree_x-trunk_width//2, tree_y-trunk_height, 
                     trunk_width, trunk_height))
    
    # Draw wavy leaves (static)
    draw_wavy_leaves(tree_x, tree_y-trunk_height, 80)

def draw_tree2(x,y):
    # Position and size
    trunk_width = 30
    trunk_height = 120
    tree_x = x
    tree_y = y
    
    pygame.draw.rect(screen, TRUNK_BROWN, 
                    (tree_x-trunk_width//2, tree_y-trunk_height, 
                     trunk_width, trunk_height))
    
    # Draw wavy leaves (static)
    draw_pine_tree(x,y)

def draw_tree3(x,y):
    # Position and size
    trunk_width = 30
    trunk_height = 120
    tree_x = x
    tree_y = y
    
    pygame.draw.rect(screen, TRUNK_BROWN, 
                    (tree_x-trunk_width//2, tree_y-trunk_height, 
                     trunk_width, trunk_height))
    
    # Draw wavy leaves (static)
    draw_dense_tree(x,y)


# Street light properties
street_lights = [
    {"x": 80, "y": 540, "on": False, "light_radius": 100, "intensity": 0.6},
    {"x": 250, "y": 540, "on": False, "light_radius": 100, "intensity": 0.6},
    {"x": 450, "y": 540, "on": False, "light_radius": 100, "intensity": 0.6},
    {"x": 750, "y": 540, "on": False, "light_radius": 100, "intensity": 0.6},
    {"x": 950, "y": 540, "on": False, "light_radius": 100, "intensity": 0.6},
    {"x": 1150, "y": 540, "on": False, "light_radius": 100, "intensity": 0.6}
]

def draw_street_light(x, y, is_on):
    # Pole (more realistic slim design)
    pygame.draw.rect(screen, (80, 80, 80), (x - 3, y - 120, 6, 80))
    
    # Light housing (modern design)
    pygame.draw.ellipse(screen, (60, 60, 60), (x - 12, y - 135, 24, 20))
    
    # Light bulb with more focused light
    if is_on:
        pygame.draw.circle(screen, (255, 240, 180), (x, y - 125), 8)

def draw_light_effect(x, y, radius, intensity):
    if is_day:
        return
    
    # Create a surface for the light effect
    light_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    # Gradient fill for the light cone
    for alpha in range(100, 0, -5):
        color = (255, 240, 180, int(alpha * intensity))
        scaled_radius = radius * alpha / 100
        pygame.draw.polygon(light_surface, color, [
            (x, y - 25),
            (x - scaled_radius//2, y + scaled_radius//2),
            (x + scaled_radius//2, y + scaled_radius//2)
        ])
    
    screen.blit(light_surface, (0, 0))


metro_sound_playing = False
traffic_sound_playing = False

# সাউন্ড লোড করা
try:
    metro_sound = pygame.mixer.Sound("metro_sound.wav")  
    traffic_sound = pygame.mixer.Sound("traffic.wav")  
    sound_available = True
except:
    print("Warning: Sound file not found, running without sound")
    sound_available = False

# Main game loop
clock = pygame.time.Clock()

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                is_day = not is_day  # Toggle day/night
                if not is_day:
                    for light in street_lights:
                        light["on"] = True
                else:
                    for light in street_lights:
                        light["on"] = False
    
    # Set colors based on day/night
    sky_color = DAY_SKY if is_day else NIGHT_SKY
    sun_color = DAY_SUN if is_day else NIGHT_MOON
    building_color = DAY_BUILDING if is_day else NIGHT_BUILDING
    window_color = DAY_WINDOW if is_day else NIGHT_WINDOW
    front_bilding_color = FRONT_BUILDING_COLOR1 if is_day else (178, 190, 195)
    front_bilding_color2 = FRONT_BUILDING_COLOR3 if is_day else (99, 110, 114)
    front_bilding_color3 = FRONT_BUILDING_COLOR2 if is_day else (178, 190, 195)
    front_bilding_window_color = (154, 236, 219) if is_day else NIGHT_WINDOW
    grass_color = DAY_GRASS if is_day else NIGHT_GRASS


    # Fill the background with sky color
    screen.fill(sky_color)

    # Draw static elements

    # Sun
    pygame.draw.circle(screen, sun_color, (200, 60), 30)


     # Cloud (only visible during day)
    if is_day:
        cloud_pos_x1 += 2.5
        if cloud_pos_x1 > WIDTH:
            cloud_pos_x1 = -200

        pygame.draw.circle(screen, WHITE, (cloud_pos_x1, 100), 30)
        pygame.draw.circle(screen, WHITE, (cloud_pos_x1 + 50, 100), 50)
        pygame.draw.circle(screen, WHITE, (cloud_pos_x1 + 100, 100), 30)

        # Cloud
        cloud_pos_x2 += 1.5
        if cloud_pos_x2 > WIDTH:
            cloud_pos_x2 = -600

        pygame.draw.circle(screen, WHITE, (cloud_pos_x2, 80), 30)
        pygame.draw.circle(screen, WHITE, (cloud_pos_x2 + 50, 80), 50)
        pygame.draw.circle(screen, WHITE, (cloud_pos_x2 + 100, 80), 30)


    # £ draw background bildings:
    pygame.draw.rect(screen, (131, 149, 167), (0, 280, WIDTH, 60))

    pygame.draw.rect(screen, building_color, (20, 80, 40, 200))
    pygame.draw.rect(screen, (131, 149, 167), (60, 80, 100, 200))

    pygame.draw.rect(screen, building_color, (280, 140, 40, 140))
    pygame.draw.rect(screen, (131, 149, 167), (320, 140, 120, 140))

    pygame.draw.rect(screen,building_color, (580, 160, 40, 120))
    pygame.draw.rect(screen, (131, 149, 167), (620, 160, 180, 120))


    pygame.draw.rect(screen, building_color, (820, 100, 40, 180))
    pygame.draw.rect(screen, (131, 149, 167), (860, 100, 100, 180))

    pygame.draw.rect(screen, building_color, (1020, 80, 40, 200))
    pygame.draw.rect(screen, (131, 149, 167), (1060, 80, 150, 200))


    # grash

    pygame.draw.rect(screen, (29, 209, 161), (0, 330, WIDTH, 160))


    # Draw buildings
    pygame.draw.rect(screen, BUILDING_COLOR, (100, 200, 60, 200))
    light_color = LIGHT_COLOR if is_day else YELLOW
    for y_pos in range(210, 370, 30):
        pygame.draw.rect(screen, window_color, (105, y_pos, 20, 20))
        pygame.draw.rect(screen, window_color, (135, y_pos, 20, 20))

    pygame.draw.rect(screen, (83, 92, 104), (200,170, 100, 210,))
    for y_pos in range(180, 340, 30):
        pygame.draw.rect(screen, window_color, (205, y_pos, 20, 20))
        pygame.draw.rect(screen, window_color, (230, y_pos, 20, 20))
        pygame.draw.rect(screen, window_color, (260, y_pos, 20, 20))

    pygame.draw.rect(screen, (71, 71, 135), (380,150, 100, 250,))
    for y_pos in range(180, 340, 30):
        pygame.draw.rect(screen, window_color, (385, y_pos, 20, 20))
        pygame.draw.rect(screen, window_color, (410, y_pos, 20, 20))
        pygame.draw.rect(screen, window_color, (440, y_pos, 20, 20))


    # Metro rail track (now in the middle of the screen)
    pygame.draw.rect(screen, METRO_TRACK_COLOR, (0, TRACK_HEIGHT, WIDTH, 20))
    pygame.draw.rect(screen, (150, 150, 150), (0, TRACK_HEIGHT+20, WIDTH, 10))  # Support structure
    
    # Draw pillars at regular intervals (shorter since track is higher)
    for x in range(50, WIDTH, 250):
        pillar_height = 100  # Shorter pillars since track is lower
        pillar_top = TRACK_HEIGHT + 30  # Start below track
        pillar_bottom = pillar_top + pillar_height
        
        # Pillar vertical beam
        pygame.draw.rect(screen, PILLAR_COLOR, (x, pillar_top, 20, pillar_height))
        # Pillar diagonal supports
        pygame.draw.line(screen, PILLAR_COLOR, (x, pillar_top), (x-15, pillar_bottom), 5)
        pygame.draw.line(screen, PILLAR_COLOR, (x+20, pillar_top), (x+35, pillar_bottom), 5)
        # Pillar base
        pygame.draw.rect(screen, PILLAR_COLOR, (x-20, pillar_bottom, 60, 15))


    # Tree (left)
    pygame.draw.polygon(screen, TREE_COLOR, [(-20, 430), (80, 430), (30, 330)])
    pygame.draw.rect(screen, (139, 69, 19), (20, 430, 20, 60))


    # footpath
    pygame.draw.rect(screen, (247, 215, 148), (0, 480, WIDTH, 80))

    # Road
    pygame.draw.rect(screen, ROAD_COLOR, (0, 530, WIDTH, 140))
    # রাস্তার মার্কিং
    for i in range(0, int(WIDTH/2), 100):
        pygame.draw.rect(screen, WHITE, (i, 581, 50, 9))

    for i in range(int(WIDTH /2 + 150), WIDTH, 100):
        pygame.draw.rect(screen, WHITE, (i, 581, 50, 9))
    # pygame.draw.rect(screen, ROAD_MIDLE, (0, 590, WIDTH, 10))


    # Metro rail body (positioned on the track)
    metro_y = TRACK_HEIGHT - 20  # Position above the track
    pygame.draw.rect(screen, METRO_COLOR, (metro_pos_x, metro_y, 400, 40))
    # Metro windows
    pygame.draw.rect(screen, window_color, (metro_pos_x + 20, metro_y + 10, 40, 20))
    pygame.draw.rect(screen, window_color, (metro_pos_x + 80, metro_y + 10, 40, 20))
    pygame.draw.rect(screen, window_color, (metro_pos_x + 140, metro_y + 10, 40, 20))
    pygame.draw.rect(screen, window_color, (metro_pos_x + 200, metro_y + 10, 40, 20))
    pygame.draw.rect(screen, window_color, (metro_pos_x + 260, metro_y + 10, 40, 20))
    pygame.draw.rect(screen, window_color, (metro_pos_x + 320, metro_y + 10, 40, 20))
    # Metro wheels
    pygame.draw.circle(screen, (0, 0, 0), (metro_pos_x + 30, metro_y + 40), 8)
    pygame.draw.circle(screen, (0, 0, 0), (metro_pos_x + 120, metro_y + 40), 8)
    pygame.draw.circle(screen, (0, 0, 0), (metro_pos_x + 250, metro_y + 40), 8)
    pygame.draw.circle(screen, (0, 0, 0), (metro_pos_x + 370, metro_y + 40), 8)


        # Metro rail (adjusted to new track position)
    metro_pos_x += 6

    # সাউন্ড কন্ট্রোল
    if sound_available:
        if -250 < metro_pos_x < (WIDTH + 400) and not metro_sound_playing:
            metro_sound.play(-1)  # লুপে সাউন্ড প্লে
            metro_sound_playing = True
        elif (metro_pos_x <= -250 or metro_pos_x >= (WIDTH + 400 )) and metro_sound_playing:
            metro_sound.stop()
            metro_sound_playing = False
    
    if metro_pos_x == WIDTH + 500:
        metro_pos_x = -1000



        # Additional buildings
    pygame.draw.rect(screen, building_color, (600,210, 100, 250,))
    pygame.draw.rect(screen, (83, 92, 104), (640,210, 100, 250,))
    for y_pos in range(240, 430, 30):
        pygame.draw.rect(screen, window_color, (645, y_pos, 20, 20))
        pygame.draw.rect(screen, window_color, (670, y_pos, 20, 20))
        pygame.draw.rect(screen, window_color, (700, y_pos, 20, 20))


    #bildings
    # 1st
    pygame.draw.rect(screen, front_bilding_color, (80,315, 130, 165,))
    pygame.draw.rect(screen, front_bilding_color2, (78,315, 135, 10,))

    pygame.draw.rect(screen, front_bilding_window_color, (95,335, 35, 35,))
    pygame.draw.rect(screen, front_bilding_window_color, (155,335, 35, 35,))
    pygame.draw.rect(screen, front_bilding_window_color, (95,380, 35, 35,))
    pygame.draw.rect(screen, front_bilding_window_color, (155,380, 35, 35,))

    pygame.draw.rect(screen, front_bilding_window_color, (125,430, 40, 50))

    pygame.draw.rect(screen, (154, 66, 219), (100,420, 10, 25))
    pygame.draw.rect(screen, (154, 150, 219), (110,420, 10, 25))
    pygame.draw.rect(screen, (154, 210, 219), (120,420, 10, 25))
    pygame.draw.rect(screen, (154, 255, 219), (130,420, 10, 25))
    pygame.draw.rect(screen, (154, 87, 219), (140,420, 10, 25))
    pygame.draw.rect(screen, (154, 134, 219), (150,420, 10, 25))
    pygame.draw.rect(screen, (154, 176, 219), (160,420, 10, 25))
    pygame.draw.rect(screen, (154, 233, 219), (170,420, 10, 25))
    pygame.draw.rect(screen, (154, 145, 219), (180,420, 10, 25))

    # 2nd: 
    pygame.draw.rect(screen, front_bilding_color2, (210,355, 160, 125,))
    pygame.draw.rect(screen, front_bilding_color3, (210,355, 160, 10,))

    pygame.draw.rect(screen, front_bilding_window_color, (225,370, 45, 35,))
    pygame.draw.rect(screen, front_bilding_window_color, (280,370, 45, 35,))

    pygame.draw.rect(screen, front_bilding_window_color, (250,420, 55, 60,))


    #3rd:
    pygame.draw.rect(screen, front_bilding_color3, (340,295, 130, 185,))
    pygame.draw.rect(screen, front_bilding_color2, (338,295, 135, 10,))


    pygame.draw.rect(screen, front_bilding_window_color, (355,310, 45, 45,))
    pygame.draw.rect(screen, front_bilding_window_color, (415,310,45, 45,))
    pygame.draw.rect(screen, front_bilding_window_color, (355,360, 45, 45,))
    pygame.draw.rect(screen, front_bilding_window_color, (415,360, 45, 45,))


    pygame.draw.rect(screen, front_bilding_window_color, (380,420, 55, 60,))
    pygame.draw.rect(screen, (154, 66, 219), (365,420, 85, 30,))


    pygame.draw.polygon(screen, (154, 66, 219), points)


    # 2nd:
    pygame.draw.rect(screen, front_bilding_color3, (710,355, 160, 125,))
    pygame.draw.rect(screen, front_bilding_color2, (710,355, 160, 10,))

    pygame.draw.rect(screen, front_bilding_window_color, (725,370, 45, 35,))
    pygame.draw.rect(screen, front_bilding_window_color, (780,370, 45, 35,))

    pygame.draw.rect(screen, front_bilding_window_color, (750,420, 55, 60,))


    #3rd:
    pygame.draw.rect(screen, front_bilding_color2, (840,275, 130, 205,))
    pygame.draw.rect(screen, front_bilding_color3, (838,295, 135, 10,))


    pygame.draw.rect(screen, front_bilding_window_color, (855,310, 45, 45,))
    pygame.draw.rect(screen, front_bilding_window_color, (915,310,45, 45,))
    pygame.draw.rect(screen, front_bilding_window_color, (855,360, 45, 45,))
    pygame.draw.rect(screen, front_bilding_window_color, (915,360, 45, 45,))


    pygame.draw.rect(screen, front_bilding_window_color, (880,420, 55, 60,))
    pygame.draw.rect(screen, (154, 66, 219), (865,420, 85, 30,))


    center_x, center_y = WIDTH // 2, HEIGHT // 2
    polygon_points = [
        (center_x + 20, center_y + 205),  # Top point
        (center_x + 120, center_y + 205),  # Top point
        (center_x + 120, center_y + 350),  # Bottom right
        (center_x - 30, center_y + 350)   # Bottom left
    ]
    zebra_points = [
        (center_x, center_y + 215),  # Top point
        (center_x + 120, center_y + 215),  # Top point
        (center_x + 120, center_y + 225),  # Bottom right
        (center_x - 30, center_y + 225)   # Bottom left
    ]


    zebra_points2 = [
        (center_x, center_y + 235),  # Top point
        (center_x + 120, center_y + 235),  # Top point
        (center_x + 120, center_y + 245),  # Bottom right
        (center_x - 30, center_y + 245)   # Bottom left
    ]
    zebra_points3 = [
        (center_x, center_y + 255),  # Top point
        (center_x + 120, center_y + 255),  # Top point
        (center_x + 120, center_y + 265),  # Bottom right
        (center_x - 2, center_y + 265)   # Bottom left
    ]

    zebra_points4 = [
        (center_x - 10, center_y + 275),  # Top point
        (center_x + 120, center_y + 275),  # Top point
        (center_x + 120, center_y + 285),  # Bottom right
        (center_x - 30, center_y + 285)   # Bottom left
    ]

    zebra_points5 = [
        (center_x - 30, center_y + 295),  # Top point
        (center_x + 120, center_y + 295),  # Top point
        (center_x + 120, center_y + 305),  # Bottom right
        (center_x - 30, center_y + 305)   # Bottom left
    ]
    zebra_points6 = [
        (center_x - 30, center_y + 315),  # Top point
        (center_x + 120, center_y + 315),  # Top point
        (center_x + 120, center_y + 325),  # Bottom right
        (center_x - 30, center_y + 325)   # Bottom left
    ]



    # # pygame.draw.polygon(screen, color, banch_points)
    pygame.draw.polygon(screen, (255, 255, 255), polygon_points)
    pygame.draw.polygon(screen, ROAD_COLOR, zebra_points)
    pygame.draw.polygon(screen, ROAD_COLOR, zebra_points2)
    pygame.draw.polygon(screen, ROAD_COLOR, zebra_points3)
    pygame.draw.polygon(screen, ROAD_COLOR, zebra_points4)
    pygame.draw.polygon(screen, ROAD_COLOR, zebra_points5)
    pygame.draw.polygon(screen, ROAD_COLOR, zebra_points6)


        # Draw street lights
    for light in street_lights:
        draw_street_light(light["x"], light["y"], light["on"] and not is_day)
        if light["on"] and not is_day:
            draw_light_effect(light["x"], light["y"] - 100, 
                             light["light_radius"], light["intensity"])

        # Traffic light (right side)
    pygame.draw.rect(screen, (50, 20, 50), (700, 390, 25, 80))  # pole
    pygame.draw.rect(screen, LIGHT_COLOR, (705, 400, 15, 15))  # red light
    pygame.draw.rect(screen, (255, 255, 0), (705, 420, 15, 15))  # yellow light
    pygame.draw.rect(screen, (0, 255, 0), (705, 440, 15, 15))  # green light
    pygame.draw.rect(screen, (50, 20, 50), (707, 460, 12, 60)) 


     # Tree (right)
    draw_tree(600,480)
    draw_tree2(30,480)
    draw_tree3(1100,480)


    #banch

    banch_points = [
        (center_x - 100, center_y + 135),  # Top point
        (center_x - 20, center_y + 135),  # Top right
        (center_x - 40, center_y + 145),  # Bottom right
        (center_x - 120, center_y + 145)   # Bottom left
    ]

    pygame.draw.rect(screen, (234,182,118), (center_x - 100, center_y + 110, 80, 30))  # up
    pygame.draw.polygon(screen, (234,182,118), banch_points)  # banch
    pygame.draw.rect(screen, (234,182,118), (center_x - 25, center_y + 135, 5, 25))  # up
    pygame.draw.rect(screen,(234,182,118), (center_x - 45, center_y + 145, 5, 20))  # up
    pygame.draw.rect(screen, (234,182,118), (center_x - 115, center_y + 145, 5, 20))  # up





    # Cars
    car1_pos_x += 3
    if car1_pos_x > WIDTH + 100:
        car1_pos_x = -100 
    car2_pos_x -= 5
    if car2_pos_x < -100:
        car2_pos_x = WIDTH + 100

    car3_pos_x += 7
    if car3_pos_x > WIDTH+100:
        car3_pos_x  = -200 

    car4_pos_x -= 4
    if car4_pos_x <-100:
        car4_pos_x  = WIDTH + 100


    draw_car(car1_pos_x,530,(149, 175, 192),50,25 )
    draw_car(car3_pos_x,550,CAR_COLOR,50,25 )
    draw_car(car2_pos_x,590,(106, 176, 76),-70,-25 )
    draw_car(car4_pos_x,610,(72, 52, 212),-70,-25 )

    # ট্রাফিক সাউন্ড কন্ট্রোল
    if sound_available:
        if not traffic_sound_playing:
            traffic_sound.play(-1)  # লুপে ট্রাফিক সাউন্ড
            traffic_sound_playing = True

    # Update the display
    pygame.display.flip()

    # Frame rate
    clock.tick(60)