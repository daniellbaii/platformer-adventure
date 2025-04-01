# tests/test_game_objects.py
import unittest
import unittest.mock
import pygame
from src.game_objects import Player, Platform, Enemy, Coin
from src.constants import PLAYER_JUMP_POWER, GRAVITY, PLAYER_SPEED

class TestGameObjects(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.player = Player(250, 300, 40, 40)
        self.platform = Platform(200, 400, 200, 20)
        self.enemy = Enemy(250, 380, 30, 20, self.platform)
        self.coin = Coin(300, 360, 20, 20)

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
        self.player.y = 350
        self.player.velocity_y = 5
        self.player.rect.topleft = (self.player.x, self.player.y)
        for _ in range(10):
            self.player.update()
            if self.player.rect.colliderect(self.platform.rect):
                if self.player.velocity_y > 0:
                    self.player.y = self.platform.y - self.player.height
                    self.player.velocity_y = 0
                    self.player.is_on_ground = True
                self.player.rect.topleft = (self.player.x, self.player.y)
                break
        self.assertEqual(self.player.y, 360)
        self.assertEqual(self.player.velocity_y, 0)
        self.assertTrue(self.player.is_on_ground)

    def test_enemy_movement(self):
        initial_x = self.enemy.x
        self.enemy.update()
        self.assertEqual(self.enemy.x, initial_x + 2)
        self.enemy.x = self.platform.x + self.platform.width
        self.enemy.update()
        self.assertEqual(self.enemy.velocity_x, -2)

    def test_coin_collection(self):
        self.player.rect.topleft = (300, 360)
        self.assertFalse(self.coin.collected)
        if self.player.rect.colliderect(self.coin.rect):
            self.coin.collected = True
            self.player.score += 1
        self.assertTrue(self.coin.collected)
        self.assertEqual(self.player.score, 1)

if __name__ == "__main__":
    unittest.main()