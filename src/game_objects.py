# src/game_objects.py
import pygame
from .constants import GRAVITY, PLAYER_JUMP_POWER, PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT

class GameObject:
    def __init__(self, x, y, width, height, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)  # Set color for rectangle

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def update(self):
        pass

class Player(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, color=(255, 255, 255))  # White
        self.velocity_x = 0
        self.velocity_y = 0
        self.jump_power = PLAYER_JUMP_POWER
        self.gravity = GRAVITY
        self.is_on_ground = False
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT]:
            dx -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            dx += PLAYER_SPEED
        self.velocity_x = dx

        if keys[pygame.K_UP] and self.is_on_ground:
            self.velocity_y = self.jump_power
            self.is_on_ground = False

        self.velocity_y += self.gravity
        if self.velocity_y > 10:
            self.velocity_y = 10

        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rect.topleft = (self.x, self.y)

class Platform(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, color=(255, 255, 255))  # White

class Enemy(GameObject):
    def __init__(self, x, y, width, height, platform):
        super().__init__(x, y, width, height, color=(255, 0, 0))  # Red
        self.velocity_x = 2  # Moves right initially
        self.platform = platform

    def update(self):
        self.x += self.velocity_x
        if self.x < self.platform.x or self.x + self.width > self.platform.x + self.platform.width:
            self.velocity_x = -self.velocity_x
        self.rect.topleft = (self.x, self.y)

class Coin(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, color=(255, 255, 0))  # Yellow
        self.collected = False