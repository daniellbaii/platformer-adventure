# src/game.py
import pygame
from .game_objects import Player, LevelOne, LevelTwo, LevelThree
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, RED, POWERUP_DURATION

class GameManager:
    """Manages the game loop, states, and objects."""
    def __init__(self):
        try:
            pygame.init()
        except Exception as e:
            print(f"Error initializing Pygame: {e}")
            raise
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Platformer Adventure")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "START"  # START, PLAYING, GAME_OVER, FINISHED
        self.levels = [LevelOne(), LevelTwo(), LevelThree()]
        self.current_level_index = 0
        self.player = Player(100, SCREEN_HEIGHT - 60, 40, 40)  # Start on ground
        self.font = pygame.font.Font(None, 36)
        self.total_coins = sum(len(level.coins) for level in self.levels)  # Total coins
        self.level_coin_counts = [0] * len(self.levels)  # Coins collected per level
        self.powerup_timer = 0  # Tracks power-up duration
        self.powerup_active = False
        self.start_time = 0  # Set to 0 before start
        self.final_time = 0  # Store final time when game is finished

    def reset_level(self):
        """Reset player and levels, handle coin counts based on state."""
        self.player.x = 100
        self.player.y = SCREEN_HEIGHT - 60  # Start on ground
        self.player.velocity_x = 0
        self.player.velocity_y = 0
        self.player.is_on_ground = True
        self.player.jump_multiplier = 1  # Reset jump boost
        self.powerup_timer = 0
        self.powerup_active = False
        if self.state == "START" or self.state == "FINISHED":
            self.level_coin_counts = [0] * len(self.levels)  # Reset all coins
        if self.state == "GAME_OVER":
            self.level_coin_counts[self.current_level_index] = 0  # Reset current level coins
        if self.state == "FINISHED":
            self.start_time = pygame.time.get_ticks()  # Reset timer for new game
        self.player.score = sum(self.level_coin_counts)  # Update score
        for level in self.levels:
            level.reset()  # Reset coins in all levels

    def handle_events(self):
        """Process user input and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if self.state == "START" and event.key == pygame.K_SPACE:
                    self.reset_level()
                    self.state = "PLAYING"
                    self.start_time = pygame.time.get_ticks()  # Start time for timer
                elif self.state == "PLAYING" and event.key == pygame.K_r:
                    self.level_coin_counts[self.current_level_index] = 0  # Reset current level coins
                    self.player.score = sum(self.level_coin_counts)  # Update score
                    self.reset_level()  # Restart current level
                elif self.state == "GAME_OVER" and event.key == pygame.K_SPACE:
                    self.reset_level()  # Restart current level
                    self.state = "PLAYING"
                elif self.state == "FINISHED" and event.key == pygame.K_SPACE:
                    self.reset_level()
                    self.state = "PLAYING"
                    self.current_level_index = 0

    def check_collisions(self):
        """Handle collisions between player and level objects."""
        current_level = self.levels[self.current_level_index]
        for platform in current_level.platforms:
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

        for enemy in current_level.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.state = "GAME_OVER"

        for coin in current_level.coins[:]:
            if not coin.collected and self.player.rect.colliderect(coin.rect):
                self.level_coin_counts[self.current_level_index] += 1
                self.player.score = sum(self.level_coin_counts)
                coin.collected = True
                current_level.coins.remove(coin)
        
        for powerup in current_level.power_ups[:]:
            if not powerup.collected and self.player.rect.colliderect(powerup.rect):
                powerup.collected = True
                current_level.power_ups.remove(powerup)
                self.player.jump_multiplier = 1.5  # Double jump height
                self.powerup_timer = pygame.time.get_ticks()
                self.powerup_active = True

        # Manage power-up timer
        if self.powerup_active:
            if pygame.time.get_ticks() - self.powerup_timer > POWERUP_DURATION:
                self.player.jump_multiplier = 1
                self.powerup_active = False

        # Transition to next level or finish
        if self.state == "PLAYING" and not current_level.coins:
            if self.current_level_index + 1 < len(self.levels):
                self.current_level_index += 1
                self.player.x = 100
                self.player.y = SCREEN_HEIGHT - 20 - 40
                self.player.velocity_x = 0
                self.player.velocity_y = 0
                self.player.is_on_ground = True
                self.player.jump_multiplier = 1
                self.powerup_timer = 0
                self.powerup_active = False
            else:
                self.final_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Store final time in seconds
                self.state = "FINISHED"

    def update(self):
        """Update game objects if in PLAYING state."""
        if self.state == "PLAYING":
            self.player.update()
            for enemy in self.levels[self.current_level_index].enemies:
                enemy.update()
            self.check_collisions()

    def render(self):
        """Draw objects and UI based on game state."""
        current_level = self.levels[self.current_level_index]
        self.screen.fill(current_level.background_color)

        if self.state == "START":
            title_text = self.font.render("Platformer Adventure", True, WHITE)
            start_text = self.font.render("Press SPACE to Start", True, WHITE)
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(start_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

        elif self.state == "PLAYING":
            self.player.draw(self.screen)
            for platform in current_level.platforms:
                platform.draw(self.screen)
            for enemy in current_level.enemies:
                enemy.draw(self.screen)
            for coin in current_level.coins:
                if not coin.collected:
                    coin.draw(self.screen)
            for powerup in current_level.power_ups:
                if not powerup.collected:
                    powerup.draw(self.screen)
            score_text = self.font.render(f"Coins: {self.player.score}/{self.total_coins}", True, WHITE)
            level_text = self.font.render(f"Level {self.current_level_index + 1}", True, WHITE)
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(level_text, (SCREEN_WIDTH - 100, 10))
            # Display timer
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Seconds with decimals
            timer_text = self.font.render(f"Time: {elapsed_time:.2f}s", True, WHITE)
            self.screen.blit(timer_text, (SCREEN_WIDTH // 2 - 50, 40))
            # Display restart instruction
            restart_text = self.font.render("Press R to Restart", True, WHITE)
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 80, 10))

        elif self.state == "GAME_OVER":
            game_over_text = self.font.render("Game Over", True, RED)
            score_text = self.font.render(f"Total Coins: {self.player.score}/{self.total_coins}", True, WHITE)
            restart_text = self.font.render("Press SPACE to Restart", True, WHITE)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(score_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50))

        elif self.state == "FINISHED":
            win_text = self.font.render("You Win!", True, WHITE)
            score_text = self.font.render(f"Total Coins: {self.player.score}/{self.total_coins}", True, WHITE)
            replay_text = self.font.render("Press SPACE to Replay", True, WHITE)
            self.screen.blit(win_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(score_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
            # Display final time
            timer_text = self.font.render(f"Time: {self.final_time:.2f}s", True, WHITE)
            self.screen.blit(timer_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(replay_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100))

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