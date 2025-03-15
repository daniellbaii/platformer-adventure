# src/game.py
import pygame
from game_objects import Player, Platform
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Platformer Adventure")
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player(100, 300, 40, 40)  # Start higher to test falling
        self.platforms = [
            Platform(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20),  # Ground platform
            Platform(200, 500, 200, 20)  # Elevated platform
        ]
        self.all_objects = [self.player] + self.platforms

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def check_collisions(self):
        for platform in self.platforms:
            if self.player.rect.colliderect(platform.rect):
                # Calculate overlaps to determine collision direction
                overlap_left = (self.player.x + self.player.width) - platform.x
                overlap_right = (platform.x + platform.width) - self.player.x
                overlap_top = (self.player.y + self.player.height) - platform.y
                overlap_bottom = (platform.y + platform.height) - self.player.y
                
                # Find the smallest overlap to resolve the collision
                min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

                # Resolve based on smallest overlap and movement direction
                if min_overlap == overlap_top and self.player.velocity_y > 0:  # Landing on top
                    self.player.y = platform.y - self.player.height
                    self.player.velocity_y = 0
                    self.player.is_on_ground = True
                elif min_overlap == overlap_bottom and self.player.velocity_y < 0:  # Hitting bottom
                    self.player.y = platform.y + platform.height
                    self.player.velocity_y = 0
                elif min_overlap == overlap_left and self.player.velocity_x > 0:  # Hitting left side
                    self.player.x = platform.x - self.player.width
                    self.player.velocity_x = 0
                elif min_overlap == overlap_right and self.player.velocity_x < 0:  # Hitting right side
                    self.player.x = platform.x + platform.width
                    self.player.velocity_x = 0
                
                # Update rect position after resolution
                self.player.rect.topleft = (self.player.x, self.player.y)

    def update(self):
        for obj in self.all_objects:
            obj.update()
        self.check_collisions()

    def render(self):
        self.screen.fill((0, 0, 0))
        for obj in self.all_objects:
            obj.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    game = GameManager()
    game.run()