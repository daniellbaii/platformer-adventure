# src/game_objects.py
import pygame
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, PLAYER_JUMP_POWER, PLAYER_SPEED, BLACK, DARK_BLUE, DARK_GREEN

class GameObject:
    """Base class for game objects with position and rendering."""
    def __init__(self, x, y, width, height, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def update(self):
        pass

class Player(GameObject):
    """Player character with movement and jumping."""
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

        # Prevent walking off edges
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.height

        self.rect.topleft = (self.x, self.y)

class Platform(GameObject):
    """Static platform for player to stand on."""
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, color=(255, 255, 255))  # White

class Enemy(GameObject):
    """Enemy that patrols a platform."""
    def __init__(self, x, y, width, height, platform):
        super().__init__(x, y, width, height, color=(255, 0, 0))  # Red
        self.velocity_x = 2
        self.platform = platform

    def update(self):
        self.x += self.velocity_x
        if self.x < self.platform.x or self.x + self.width > self.platform.x + self.platform.width:
            self.velocity_x = -self.velocity_x
        self.rect.topleft = (self.x, self.y)

class Coin(GameObject):
    """Collectible coin that increases score."""
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, color=(255, 255, 0))  # Yellow
        self.collected = False

class Level:
    """Base class for managing level-specific objects."""
    def __init__(self):
        self.platforms = []
        self.enemies = []
        self.coins = []
        self.initial_coins = []  # Store initial coin configurations
        self.background_color = BLACK

    def get_objects(self):
        """Return all objects for rendering and updating."""
        return [self.platforms, self.enemies, self.coins]

    def reset(self):
        """Reset objects to initial state."""
        self.coins = [Coin(coin.x, coin.y, coin.width, coin.height) for coin in self.initial_coins]

class LevelOne(Level):
    """First level configuration."""
    def __init__(self):
        super().__init__()
        self.platforms = [
            Platform(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20),  # Ground
            Platform(400, 500, 200, 20)  # Elevated
        ]
        self.enemies = [Enemy(450, 480, 30, 20, self.platforms[1])]
        self.coins = [
            Coin(500, 460, 20, 20),
            Coin(300, SCREEN_HEIGHT - 40, 20, 20)
        ]
        self.initial_coins = self.coins.copy()  # Store initial coins
        self.background_color = BLACK

class LevelTwo(Level):
    """Second level configuration."""
    def __init__(self):
        super().__init__()
        self.platforms = [
            Platform(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20),  # Ground
            Platform(500, 420, 200, 20),  # Higher platform
            Platform(250, 500, 150, 20)  # Lower platform
        ]
        self.enemies = [
            Enemy(550, 400, 30, 20, self.platforms[1]),  # On higher platform
            Enemy(300, 480, 30, 20, self.platforms[2])  # On lower platform
        ]
        self.coins = [
            Coin(600, 380, 20, 20),  # Above higher platform
            Coin(325, 460, 20, 20)  # Above lower platform
        ]
        self.initial_coins = self.coins.copy()  # Store initial coins
        self.background_color = DARK_BLUE

class LevelThree(Level):
    """Second level configuration."""
    def __init__(self):
        super().__init__()
        self.platforms = [
            Platform(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20),  # Ground
            Platform(450, 280, 50, 20),  # Highest platform
            Platform(220, 340, 100, 20),  # Higher platform
            Platform(500, 420, 200, 20),  # High platform
            Platform(250, 500, 150, 20)  # Lower platform
        ]
        self.enemies = [
            Enemy(550, 400, 30, 20, self.platforms[3]),  # On higher platform
            Enemy(300, 480, 30, 20, self.platforms[4])  # On lower platform
        ]
        self.coins = [
            Coin(475, 240, 20, 20),  # Above highest platform
            Coin(600, 380, 20, 20),  # Above high platform
            Coin(325, 460, 20, 20)  # Above lower platform
        ]
        self.initial_coins = self.coins.copy()  # Store initial coins
        self.background_color = DARK_GREEN