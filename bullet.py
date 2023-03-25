# bullet.py

import pygame
from config import SCREEN_HEIGHT

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, bullet_img):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.move_ip(0, self.direction * 10)
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
