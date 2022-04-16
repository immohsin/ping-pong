import os
import unittest

# Set env before importing config
os.environ["CONFIG_PATH"] = "config/player1-static.yml"
from player.config import PlayerConfig


class PlayerConfigTest(unittest.TestCase):
    def test_player_config(self):
        cfg = PlayerConfig.read_config()

        self.assertEqual(cfg.get_player_name(), "Joey")

        self.assertEqual(cfg.get_player_defence_length(), 8)

        self.assertEqual(cfg.get_referee_host(), "http://referee:9090")

        self.assertEqual(cfg.get_port(), 8081)

        self.assertEqual(cfg.get_pubstore(), {"redis": {"host": "redis", "port": 6379}})


if __name__ == "__main__":
    unittest.main()
