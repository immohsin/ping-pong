import requests
from random import sample, randint

from player.utils.urlbuilder import (
    get_notify_attack_url,
    get_join_championship_url,
    get_notify_status,
)


class PlayerImpl:
    def __init__(self, config, logger) -> None:
        self.config = config
        self.logger = logger
        self.player_name = self.config.get_player_name()
        self.referee_host = self.config.get_referee_host()
        self.defence_length = self.config.get_player_defence_length()

    def read_game_instructions(self, data):
        if data["attacker"] == self.player_name:
            self.start_attack(data["opponent"], data["game-id"])

    def start_attack(self, opponent, game_id):
        random_number = randint(1, 10)
        self.logger.info(
            f"{self.player_name} random number selected is {random_number}"
        )
        self._notify_attack_2_referee(random_number, opponent, game_id)

    def _notify_attack_2_referee(self, random_number, opponent, game_id):
        url = get_notify_attack_url(game_id, random_number, opponent)
        requests.get(url)

    def join_championship(self):
        url = get_join_championship_url(self.player_name)
        requests.get(url)

    def defend_number(self, data):
        opponent_defence_list = set(sample(range(1, 11), self.defence_length))
        defended = int(data["guessed_number"]) in opponent_defence_list
        game_id = data["game-id"]
        self.logger.info(
            f"{self.player_name} defence list: {opponent_defence_list} and its defended={defended}"
        )
        url = get_notify_status(game_id, defended)
        requests.get(url)
