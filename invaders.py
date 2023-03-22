import pygame
import sys
import random
from pygame.locals import *

pygame.init()


# Initialize the Pygame module, define constants, and load the sprites
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
FPS = 60
ALIEN_COLUMNS = 11
ALIEN_ROWS = 5
ALIEN_SPACING = 40
SCORE = 0

ALIEN_SPEED = 2
ALIEN_DROP = 30
ALIEN_SHOOT_PROB = 0.01
SPEED_INCREASE_FACTOR = 1.25
SHOOT_PROB_INCREASE_FACTOR = 1.25


scale_factor = 0.4
ALIEN_SPACING = int(ALIEN_SPACING * scale_factor)


player_img = pygame.image.load("player.png")
bullet_img = pygame.image.load("bullet.png")
alien1_img = pygame.image.load("alien1.png")
alien2_img = pygame.image.load("alien2.png")
alien3_img = pygame.image.load("alien3.png")
alien4_img = pygame.image.load("alien4.png")

player_img = pygame.transform.scale(player_img, (int(player_img.get_width() * scale_factor), int(player_img.get_height() * scale_factor)))
bullet_img = pygame.transform.scale(bullet_img, (int(bullet_img.get_width() * scale_factor), int(bullet_img.get_height() * scale_factor)))
alien1_img = pygame.transform.scale(alien1_img, (int(alien1_img.get_width() * scale_factor), int(alien1_img.get_height() * scale_factor)))
alien2_img = pygame.transform.scale(alien2_img, (int(alien2_img.get_width() * scale_factor), int(alien2_img.get_height() * scale_factor)))
alien3_img = pygame.transform.scale(alien3_img, (int(alien3_img.get_width() * scale_factor), int(alien3_img.get_height() * scale_factor)))
alien4_img = pygame.transform.scale(alien4_img, (int(alien4_img.get_width() * scale_factor), int(alien4_img.get_height() * scale_factor)))

alien_imgs = [alien1_img, alien2_img, alien2_img, alien3_img, alien4_img]

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


# Initialize the game objects, and create the main game loop:

import itertools
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

while True:
    screen.fill(WHITE)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE:
            bullet = Bullet(player.rect.centerx, player.rect.top, -1)
            bullets.add(bullet)

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
    SCORE += len(aliens_hit) * 10

    if random.random() < alien_shoot_prob:
        alien_shooter = random.choice(aliens.sprites())
        alien_bullet = Bullet(alien_shooter.rect.centerx, alien_shooter.rect.bottom, 1)
        bullets.add(alien_bullet)

    if pygame.sprite.spritecollide(player, bullets, False) or any(alien.rect.colliderect(player.rect) for alien in aliens):
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
