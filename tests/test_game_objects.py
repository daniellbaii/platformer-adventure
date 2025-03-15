# tests/test_game_objects.py
import unittest
import unittest.mock
import pygame
from src.game_objects import Player, Platform
from src.constants import PLAYER_JUMP_POWER, GRAVITY, PLAYER_SPEED

class TestGameObjects(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.player = Player(250, 300, 40, 40)  # x overlaps platform
        self.platform = Platform(200, 400, 200, 20)

    def test_player_jump(self):
        self.player.is_on_ground = True
        keys = {pygame.K_UP: True, pygame.K_LEFT: False, pygame.K_RIGHT: False}
        with unittest.mock.patch('pygame.key.get_pressed', return_value=keys):
            self.player.update()
            self.assertEqual(self.player.velocity_y, PLAYER_JUMP_POWER + GRAVITY)
            self.assertFalse(self.player.is_on_ground)

    def test_gravity_application(self):
        initial_velocity = self.player.velocity_y
        self.player.update()
        self.assertEqual(self.player.velocity_y, initial_velocity + GRAVITY)

    def test_horizontal_movement(self):
        keys = {pygame.K_RIGHT: True, pygame.K_LEFT: False, pygame.K_UP: False}
        with unittest.mock.patch('pygame.key.get_pressed', return_value=keys):
            initial_x = self.player.x
            self.player.update()
            self.assertEqual(self.player.x, initial_x + PLAYER_SPEED)

    def test_collision_landing(self):
        self.player.y = 350  # Above platform
        self.player.velocity_y = 5  # Falling
        self.player.rect.topleft = (self.player.x, self.player.y)
        
        # Simulate falling until collision (mimicking game loop)
        for _ in range(10):  # Enough frames to reach platform
            self.player.update()
            if self.player.rect.colliderect(self.platform.rect):
                if self.player.velocity_y > 0:  # Falling onto platform
                    self.player.y = self.platform.y - self.player.height
                    self.player.velocity_y = 0
                    self.player.is_on_ground = True
                self.player.rect.topleft = (self.player.x, self.player.y)
                break
        
        self.assertEqual(self.player.y, 360)  # 400 - 40
        self.assertEqual(self.player.velocity_y, 0)
        self.assertTrue(self.player.is_on_ground)

if __name__ == "__main__":
    unittest.main()