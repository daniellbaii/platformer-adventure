# src/game.py
import pygame
from .game_objects import Player, Platform, Enemy, Coin
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class GameManager:
    """Manages the game loop, objects, and state."""
    def __init__(self):
        try:
            pygame.init()
        except Exception as e:
            print(f"Error initializing Pygame: {e}")
            raise
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Platformer Adventure")
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player(100, 300, 40, 40)
        self.platforms = [
            Platform(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20),  # Ground
            Platform(200, 500, 200, 20)  # Elevated
        ]
        self.enemies = [Enemy(250, 480, 30, 20, self.platforms[1])]
        self.coins = [
            Coin(300, 460, 20, 20),
            Coin(50, SCREEN_HEIGHT - 40, 20, 20)
        ]
        self.all_objects = [self.player] + self.platforms + self.enemies + self.coins
        self.game_over = False

    def handle_events(self):
        """Process user input and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def check_collisions(self):
        """Handle collisions between player and platforms, enemies, coins."""
        for platform in self.platforms:
            if self.player.rect.colliderect(platform.rect):
                overlap_left = (self.player.x + self.player.width) - platform.x
                overlap_right = (platform.x + platform.width) - self.player.x
                overlap_top = (self.player.y + self.player.height) - platform.y
                overlap_bottom = (platform.y + platform.height) - self.player.y
                min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
                if min_overlap == overlap_top and self.player.velocity_y > 0:
                    self.player.y = platform.y - self.player.height
                    self.player.velocity_y = 0
                    self.player.is_on_ground = True
                elif min_overlap == overlap_bottom and self.player.velocity_y < 0:
                    self.player.y = platform.y + platform.height
                    self.player.velocity_y = 0
                elif min_overlap == overlap_left and self.player.velocity_x > 0:
                    self.player.x = platform.x - self.player.width
                    self.player.velocity_x = 0
                elif min_overlap == overlap_right and self.player.velocity_x < 0:
                    self.player.x = platform.x + platform.width
                    self.player.velocity_x = 0
                self.player.rect.topleft = (self.player.x, self.player.y)

        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.game_over = True
                print("Game Over! You hit an enemy.")

        for coin in self.coins[:]:
            if not coin.collected and self.player.rect.colliderect(coin.rect):
                self.player.score += 1
                coin.collected = True
                self.coins.remove(coin)
                print(f"Score: {self.player.score}")

    def update(self):
        """Update all game objects if game not over."""
        if not self.game_over:
            for obj in self.all_objects:
                if not isinstance(obj, Coin) or not obj.collected:
                    obj.update()
            self.check_collisions()

    def render(self):
        """Draw all objects and UI to the screen."""
        self.screen.fill((0, 0, 0))
        for obj in self.all_objects:
            if not isinstance(obj, Coin) or not obj.collected:
                obj.draw(self.screen)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.player.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        if self.game_over:
            game_over_text = font.render("Game Over", True, (255, 0, 0))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    try:
        game = GameManager()
        game.run()
    except Exception as e:
        print(f"Game failed to start: {e}")