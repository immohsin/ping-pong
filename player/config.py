import os
import yaml


CONFIG_PATH = os.environ.get("CONFIG_PATH")


class PlayerConfig:
    _instance = None

    def __init__(self, config):
        self.config = config

    @staticmethod
    def read_config():
        with open(CONFIG_PATH) as f:
            cfg = yaml.load(f.read(), Loader=yaml.Loader)
        return PlayerConfig.init_config(cfg)

    @staticmethod
    def init_config(cfg):
        PlayerConfig._instance = PlayerConfig(cfg)
        return PlayerConfig._instance

    @staticmethod
    def instance():
        if not PlayerConfig._instance:
            raise RuntimeError("Config should be initialized before use")

        return PlayerConfig._instance

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

    def get_player_name(self):
        return self.get_property("name")

    def get_player_defence_length(self):
        return self.get_property("defence-length")

    def get_referee_host(self):
        return self.get_property("referee-host")

    def get_pubstore(self):
        return self.get_multilevel_property("pubsub", "store")

    def get_port(self):
        return self.get_property("player-port")
