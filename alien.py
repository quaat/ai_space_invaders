# alien.py

import pygame
import math


class Alien(pygame.sprite.Sprite):
    def __init__(self, alien_type, x, y, speed, alien_img):
        super().__init__()
        self.original_image = alien_img
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = alien_type
        self.animation_time = 0
        self.speed = speed
        self.animation_speed = 60

    def update(self):
        self.animation_time += 1
        angle = math.sin(self.animation_time / self.animation_speed) * 10
        scale_factor = (
            1 + math.sin(self.animation_time / (self.animation_speed * 2)) * 0.05
        )

        rotated_image = pygame.transform.rotate(self.original_image, angle)

        scaled_width = int(self.original_image.get_width() * scale_factor)
        scaled_height = int(self.original_image.get_height() * scale_factor)
        scaled_image = pygame.transform.scale(
            rotated_image, (scaled_width, scaled_height)
        )

        self.image = scaled_image

        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.x += self.speed

    def change_direction(self):
        self.speed = -self.speed
        self.rect.y += 20
