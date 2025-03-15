# src/game_objects.py
import pygame
from src.constants import GRAVITY, PLAYER_JUMP_POWER, PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT

class GameObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

    def update(self):
        pass

class Player(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.velocity_x = 0
        self.velocity_y = 0
        self.jump_power = PLAYER_JUMP_POWER  # -10
        self.gravity = GRAVITY  # 0.5
        self.is_on_ground = False

    def update(self):
        # Get keypresses for continuous input
        keys = pygame.key.get_pressed()
        
        # Calculate horizontal movement (dx)
        dx = 0
        if keys[pygame.K_LEFT]:
            dx -= PLAYER_SPEED  # -5
        if keys[pygame.K_RIGHT]:
            dx += PLAYER_SPEED  # 5
        self.velocity_x = dx

        # Handle jumping with UP key
        if keys[pygame.K_UP] and self.is_on_ground:
            self.velocity_y = self.jump_power
            self.is_on_ground = False

        # Apply gravity
        self.velocity_y += self.gravity
        if self.velocity_y > 10:  # Cap falling speed
            self.velocity_y = 10

        # Update position (no boundary checks here)
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rect.topleft = (self.x, self.y)

class Platform(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)