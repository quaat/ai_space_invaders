import pygame


class Shield(pygame.sprite.Sprite):
    def __init__(self, x, y, shield_img):
        super().__init__()
        self.original_image = shield_img
        self.image = shield_img.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 100  # You can adjust the health of the shield

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
        else:
            self.update_transparency()

    def update_transparency(self):
        alpha = int((self.health / 100) * 255)
        self.image = self.original_image.copy()
        self.image.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
