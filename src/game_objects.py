# src/game_objects.py
import pygame
from constants import GRAVITY, PLAYER_JUMP_POWER, SCREEN_HEIGHT, PLAYER_SPEED

class GameObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)  # For collision detection

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)  # White rectangle as placeholder

    def update(self):
        pass  # To be overridden by subclasses

class Player(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_on_ground = False

    def update(self):
        # Apply gravity
        self.velocity_y += GRAVITY
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rect.topleft = (self.x, self.y)  # Update rect position

        # Prevent falling off screen (temporary boundary)
        if self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
            self.velocity_y = 0
            self.is_on_ground = True

    def jump(self):
        if self.is_on_ground:
            self.velocity_y = PLAYER_JUMP_POWER
            self.is_on_ground = False

class Platform(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def update(self):
        pass  # Platforms are static for now