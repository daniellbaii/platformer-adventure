# src/game.py
import pygame
from game_objects import Player, Platform
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PLAYER_SPEED

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Platformer Adventure")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize game objects
        self.player = Player(100, SCREEN_HEIGHT - 50, 40, 40)  # Player starts near bottom
        self.platforms = [Platform(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20)]  # Ground platform
        self.all_objects = [self.player] + self.platforms

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.velocity_x = -PLAYER_SPEED
                elif event.key == pygame.K_RIGHT:
                    self.player.velocity_x = PLAYER_SPEED
                elif event.key == pygame.K_UP:
                    self.player.jump()
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    self.player.velocity_x = 0

    def update(self):
        for obj in self.all_objects:
            obj.update()

    def render(self):
        self.screen.fill((0, 0, 0))  # Black background
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