import os
import unittest

# Set env before importing config
os.environ["CONFIG_PATH"] = "config/referee-static.yml"
from referee.config import RefereeConfig


class RefreeConfigTest(unittest.TestCase):
    def test_player_config(self):
        cfg = RefereeConfig.read_config()

        self.assertEqual(
            cfg.get_players(),
            {
                "Joey": "http://localhost:8081",
                "Gunther": "http://localhost:8082",
                "Russel": "http://localhost:8083",
                "Ross": "http://localhost:8084",
                "Monica": "http://localhost:8085",
                "Rachel": "http://localhost:8086",
                "Phoebe": "http://localhost:8087",
                "Chandler": "http://localhost:8088",
            },
        )

        self.assertEqual(cfg.get_winning_score(), 5)

        self.assertEqual(cfg.get_game_state_store(), {"memory": None})

        self.assertEqual(cfg.get_port(), 9090)

        self.assertEqual(cfg.get_pubstore(), {"redis": {"host": "redis", "port": 6379}})


if __name__ == "__main__":
    unittest.main()
