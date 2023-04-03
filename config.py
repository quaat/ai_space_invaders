# config.py

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
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
SPEED_INCREASE = 0.25
SHOOT_PROB_INCREASE_FACTOR = 1.25

# Scale factor
scale_factor = 0.3
ALIEN_SPACING = int(ALIEN_SPACING * scale_factor)

# Dimensions
alien_width = int(SCREEN_WIDTH * 0.05)
shield_width = int(SCREEN_WIDTH * 0.1)
player_width = int(SCREEN_WIDTH * 0.06)
