# main.py

import sys
import pygame
import random
import itertools
from pygame.locals import *
from config import (
    ALIEN_COLUMNS,
    ALIEN_DROP,
    ALIEN_ROWS,
    ALIEN_SPEED,
    ALIEN_SHOOT_PROB,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SHOOT_PROB_INCREASE_FACTOR,
    SPEED_INCREASE,
    WHITE,
    BLACK,
    FPS,
    ALIEN_SPACING,
    alien_width,
)

from player import Player
from bullet import Bullet
from alien import Alien
from shield import Shield

pygame.init()
pygame.mixer.init()
fullscreen = True


def resize_image(image, new_width):
    aspect_ratio = image.get_height() / image.get_width()
    new_height = int(new_width * aspect_ratio)
    return pygame.transform.scale(image, (new_width, new_height))


def load_image(filename):
    return pygame.image.load(filename)


def draw_text(surface, text, size, x, y, color=(255, 255, 255)):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

SCORE = 0

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

alien_imgs = [alien1_img, alien2_img, alien2_img, alien3_img, alien4_img]

player_img = pygame.transform.scale(
    player_img,
    (
        int(player_img.get_width() * 1),
        int(player_img.get_height() * 1),
    ),
)
bullet_img = pygame.transform.scale(
    bullet_img,
    (
        int(bullet_img.get_width() * 0.4),
        int(bullet_img.get_height() * 0.4),
    ),
)


shield_img = pygame.image.load("assets/shield.png")
shield_width = int(SCREEN_WIDTH * 0.1)  # Adjust the size to your preference
shield_img = resize_image(shield_img, shield_width)


# Load the sound effects
shoot_sound = pygame.mixer.Sound("assets/shoot.wav")
invaderkilled_sound = pygame.mixer.Sound("assets/invaderkilled.wav")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")


# Define a function to display the welcome screen
def welcome_screen(last_score, high_score):
    global fullscreen
    global screen
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
                if event.key == K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode(
                            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN
                        )
                    else:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.display.flip()
        clock.tick(FPS)


# Initialize the game objects, and create the main game loop:

last_score = 0
high_score = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.display.set_caption("Space Invaders")

player = Player(player_img)
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()


# Create and position the shield instances
def setup_shields():
    shields = pygame.sprite.Group()

    shield_count = 3
    shield_spacing = SCREEN_WIDTH / 6
    start_x = (
        SCREEN_WIDTH - shield_count * shield_width - (shield_count - 1) * shield_spacing
    ) // 2
    start_y = SCREEN_HEIGHT - (SCREEN_HEIGHT * 0.2)

    for i in range(shield_count):
        x = start_x + i * (shield_width + shield_spacing)
        y = start_y
        shield = Shield(x, y, shield_img)
        shields.add(shield)

    return shields


import contextlib

for row, col in itertools.product(range(ALIEN_ROWS), range(ALIEN_COLUMNS)):
    x = col * (alien_imgs[row].get_width() + ALIEN_SPACING)
    y = row * (alien_imgs[row].get_height() + ALIEN_SPACING)
    alien = Alien(row, x, y, ALIEN_SPEED, alien_imgs[row])
    aliens.add(alien)

alien_shoot_prob = ALIEN_SHOOT_PROB

if not welcome_screen(last_score, high_score):
    pygame.quit()
    sys.exit()

shields = setup_shields()
while True:
    screen.blit(game_bg, (0, 0))
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE:
            bullet = Bullet(player.rect.centerx, player.rect.top, -1, bullet_img)
            bullets.add(bullet)
            shoot_sound.play()

    player.update(keys)
    aliens.update()
    bullets.update()

    aliens_moved_down = False
    for alien in aliens:
        if (alien.rect.right >= SCREEN_WIDTH or alien.rect.left <= 0) and not aliens_moved_down:
            for a in aliens:
                a.change_direction()
            aliens_moved_down = True
            break
    else:
        aliens_moved_down = False


    aliens_hit = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if aliens_hit:
        invaderkilled_sound.play()
    SCORE += len(aliens_hit) * 10
    draw_text(screen, f"Score: {SCORE}", int(SCREEN_WIDTH / 30), SCREEN_WIDTH - 300, 10)

    shields_hit = pygame.sprite.groupcollide(shields, bullets, False, True)
    for shield in shields_hit:
        shield.hit(25)  # Adjust the damage value based on your preference

    if random.random() < alien_shoot_prob:
        with contextlib.suppress(IndexError):
            alien_shooter = random.choice(aliens.sprites())
            alien_bullet = Bullet(
                alien_shooter.rect.centerx, alien_shooter.rect.bottom, 1, bullet_img
            )
            bullets.add(alien_bullet)
    if pygame.sprite.spritecollide(player, bullets, False) or any(
        alien.rect.colliderect(player.rect) for alien in aliens
    ):
        explosion_sound.play()
        pygame.mixer.music.stop()
        pygame.time.delay(3000)  # Wait for 3 seconds (3000 milliseconds)
        last_score = SCORE
        high_score = max(high_score, last_score)
        shields = setup_shields()
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
                alien = Alien(row, x, y, ALIEN_SPEED, alien_imgs[row])
                aliens.add(alien)
        if not welcome_screen(last_score, high_score):
            pygame.quit()
            sys.exit()

    if not aliens:
        ALIEN_SPEED += SPEED_INCREASE
        alien_shoot_prob *= SHOOT_PROB_INCREASE_FACTOR
        for row in range(ALIEN_ROWS):
            for col in range(ALIEN_COLUMNS):
                x = col * (alien_imgs[row].get_width() + ALIEN_SPACING)
                y = row * (alien_imgs[row].get_height() + ALIEN_SPACING)
                alien = Alien(row, x, y, ALIEN_SPEED, alien_imgs[row])
                aliens.add(alien)

    aliens.draw(screen)
    bullets.draw(screen)
    shields.draw(screen)
    screen.blit(player.image, player.rect)

    pygame.display.flip()
    clock.tick(FPS)
