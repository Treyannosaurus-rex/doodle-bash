import pygame

from Flying_Eye import FLying_Eye
from Wizard import Wizard

pygame.init()

#create game window
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 840

screen = pygame.display.set_mode ((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Doodle Bash")

#enable V-Sync
pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF|pygame.HWSURFACE)

#set framerate
clock = pygame.time.Clock()
FPS = 65

#colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#define game variables
intro_count = 0
last_count_update = pygame.time.get_ticks()

#define character variablesjl
EYE_SIZE = 149.9
EYE_SCALE = 3.30
EYE_OFFSET = [65.5, 55]
EYE_DATA = [EYE_SIZE, EYE_SCALE, EYE_OFFSET]

WIZARD_SIZE = 149.9
WIZARD_SCALE = 3.45
WIZARD_OFFSET = [63.8, 46.5]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#load background image - stage 1
bg_image = pygame.image.load("assets/images/stage.png").convert_alpha()

#load spritesheets
eye_sheet = pygame.image.load("assets/images/character_sprites/Flying eye/Flying Eye.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/character_sprites/Wizard Pack/Wizard.png").convert_alpha()

#define number of steps in each animation
EYE_ANIMATION_STEPS = [8, 8, 8, 8, 4, 4, 4]
WIZARD_ANIMATION_STEPS = [6, 8, 8, 8, 4, 4, 6]

#function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

#function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

#create instances of fighters
fighter_1 = FLying_Eye(355, 472, False, EYE_DATA, eye_sheet, EYE_ANIMATION_STEPS)
fighter_2 = Wizard(1004, 472, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)

#game loop
run = True
while run:

    clock.tick(FPS)

    #draw background
    draw_bg()

    #show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 1020, 20)

    if intro_count <= 0:
        #move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1)
    else:
        #update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
        print(intro_count)

    #update fighters
    fighter_1.update()
    fighter_2.update()

    #draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.update()

#exit pygame
pygame.quit()
