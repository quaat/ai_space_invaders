import pygame
import sys
import random
from pygame.locals import *

pygame.init()
pygame.mixer.init()


# Initialize the Pygame module, define constants, and load the sprites
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
ALIEN_COLUMNS = 11
ALIEN_ROWS = 5
ALIEN_SPACING = 40
SCORE = 0

ALIEN_SPEED = 1
ALIEN_DROP = 30
ALIEN_SHOOT_PROB = 0.01
SPEED_INCREASE_FACTOR = 1.25
SHOOT_PROB_INCREASE_FACTOR = 1.25


scale_factor = 0.3
ALIEN_SPACING = int(ALIEN_SPACING * scale_factor)

alien_width = int(SCREEN_WIDTH * 0.05)


def resize_image(image, new_width):
    aspect_ratio = image.get_height() / image.get_width()
    new_height = int(new_width * aspect_ratio)
    return pygame.transform.scale(image, (new_width, new_height))


def load_image(filename):
    return pygame.image.load(filename)


welcome_bg = pygame.image.load("assets/welcome_bg.png")
welcome_bg = pygame.transform.scale(welcome_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

player_img = pygame.image.load("assets/player.png")
bullet_img = pygame.image.load("assets/bullet.png")
game_bg = pygame.transform.scale(
    load_image("assets/game_bg.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
)
alien1_img = resize_image(load_image("assets/alien1.png"), alien_width)
alien2_img = resize_image(load_image("assets/alien2.png"), alien_width)
alien3_img = resize_image(load_image("assets/alien3.png"), alien_width)
alien4_img = resize_image(load_image("assets/alien4.png"), alien_width)


player_img = pygame.transform.scale(
    player_img,
    (
        int(player_img.get_width() * scale_factor),
        int(player_img.get_height() * scale_factor),
    ),
)
bullet_img = pygame.transform.scale(
    bullet_img,
    (
        int(bullet_img.get_width() * scale_factor),
        int(bullet_img.get_height() * scale_factor),
    ),
)

alien_imgs = [alien1_img, alien2_img, alien2_img, alien3_img, alien4_img]

# Load the sound effects
shoot_sound = pygame.mixer.Sound("assets/shoot.wav")
invaderkilled_sound = pygame.mixer.Sound("assets/invaderkilled.wav")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")


# Define the classes for the game objects


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)

    def update(self, keys):
        if keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if keys[K_RIGHT]:
            self.rect.move_ip(5, 0)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.move_ip(0, self.direction * 10)
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Alien(pygame.sprite.Sprite):
    def __init__(self, alien_type, x, y, speed):
        super().__init__()
        self.image = alien_imgs[alien_type]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed


# Define a function to display the welcome screen
def welcome_screen(last_score, high_score):
    font = pygame.font.Font(None, 36)

    welcome_text = "Press 'P' to play or 'Q' to quit"
    welcome_text_surface = font.render(welcome_text, True, WHITE)
    welcome_text_rect = welcome_text_surface.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    )

    score_text = f"Last Score: {last_score} High Score: {high_score}"
    score_text_surface = font.render(score_text, True, WHITE)
    score_text_rect = score_text_surface.get_rect(
        center=(SCREEN_WIDTH // 2, welcome_text_rect.y - 50)
    )

    while True:
        screen.blit(welcome_bg, (0, 0))
        screen.blit(welcome_text_surface, welcome_text_rect)
        screen.blit(score_text_surface, score_text_rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_p:
                    return True
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(FPS)


# Initialize the game objects, and create the main game loop:

import itertools

last_score = 0
high_score = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Space Invaders")

player = Player()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()

for row, col in itertools.product(range(ALIEN_ROWS), range(ALIEN_COLUMNS)):
    x = col * (alien_imgs[row].get_width() + ALIEN_SPACING)
    y = row * (alien_imgs[row].get_height() + ALIEN_SPACING)
    alien = Alien(row, x, y, ALIEN_SPEED)
    aliens.add(alien)

alien_shoot_prob = ALIEN_SHOOT_PROB

if not welcome_screen(last_score, high_score):
    pygame.quit()
    sys.exit()

while True:
    screen.blit(game_bg, (0, 0))
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE:
            bullet = Bullet(player.rect.centerx, player.rect.top, -1)
            bullets.add(bullet)
            shoot_sound.play()

    player.update(keys)
    aliens.update()
    bullets.update()

    for alien in aliens:
        if alien.rect.right >= SCREEN_WIDTH or alien.rect.left <= 0:
            for a in aliens:
                a.speed = -a.speed
                a.rect.y += ALIEN_DROP
            break

    aliens_hit = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if aliens_hit:
        invaderkilled_sound.play()
    SCORE += len(aliens_hit) * 10

    if random.random() < alien_shoot_prob:
        alien_shooter = random.choice(aliens.sprites())
        alien_bullet = Bullet(alien_shooter.rect.centerx, alien_shooter.rect.bottom, 1)
        bullets.add(alien_bullet)

    if pygame.sprite.spritecollide(player, bullets, False) or any(
        alien.rect.colliderect(player.rect) for alien in aliens
    ):
        explosion_sound.play()
        pygame.time.delay(3000)  # Wait for 3 seconds (3000 milliseconds)
        last_score = SCORE
        high_score = max(high_score, last_score)
        SCORE = 0
        ALIEN_SPEED = 2
        alien_shoot_prob = ALIEN_SHOOT_PROB
        player.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)
        bullets.empty()
        aliens.empty()
        for row in range(ALIEN_ROWS):
            for col in range(ALIEN_COLUMNS):
                x = col * (alien_imgs[row].get_width() + ALIEN_SPACING)
                y = row * (alien_imgs[row].get_height() + ALIEN_SPACING)
                alien = Alien(row, x, y, ALIEN_SPEED)
                aliens.add(alien)
        if not welcome_screen(last_score, high_score):
            pygame.quit()
            sys.exit()

    if not aliens:
        ALIEN_SPEED *= SPEED_INCREASE_FACTOR
        alien_shoot_prob *= SHOOT_PROB_INCREASE_FACTOR
        for row in range(ALIEN_ROWS):
            for col in range(ALIEN_COLUMNS):
                x = col * (alien_imgs[row].get_width() + ALIEN_SPACING)
                y = row * (alien_imgs[row].get_height() + ALIEN_SPACING)
                alien = Alien(row, x, y, ALIEN_SPEED)
                aliens.add(alien)

    aliens.draw(screen)
    bullets.draw(screen)
    screen.blit(player.image, player.rect)

    pygame.display.flip()
    clock.tick(FPS)
