import os
import yaml


CONFIG_PATH = os.environ.get("CONFIG_PATH")


class RefereeConfig:
    _instance = None

    def __init__(self, config):
        self.config = config

    @staticmethod
    def read_config():
        with open(CONFIG_PATH) as f:
            cfg = yaml.load(f.read(), Loader=yaml.Loader)
        return RefereeConfig.init_config(cfg)

    @staticmethod
    def init_config(cfg):
        RefereeConfig._instance = RefereeConfig(cfg)
        return RefereeConfig._instance

    @staticmethod
    def instance():
        if not RefereeConfig._instance:
            raise RuntimeError("Config should be initialized before use")

        return RefereeConfig._instance

    def get_property(self, section):
        try:
            return self.config[section]
        except KeyError:
            return None

    def get_multilevel_property(self, section, key):
        try:
            return self.config[section][key]
        except KeyError:
            return None

    def get_players(self):
        return self.get_property("players")

    def get_winning_score(self):
        return self.get_property("winning-score")

    def get_pubstore(self):
        return self.get_multilevel_property("pubsub", "store")

    def get_game_state_store(self):
        return self.get_multilevel_property("game-state", "store")

    def get_port(self):
        return self.get_property("referee-port")
