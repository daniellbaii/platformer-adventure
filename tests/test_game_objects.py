# tests/test_game_objects.py
import unittest
from src.game_objects import Player

class TestGameObjects(unittest.TestCase):
    def test_player_jump(self):
        player = Player(0, 0, 40, 40)
        player.is_on_ground = True
        player.jump()
        self.assertEqual(player.velocity_y, -10)  # Jump power from constants

if __name__ == "__main__":
    unittest.main()