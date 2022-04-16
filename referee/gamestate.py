import uuid
from collections import defaultdict
from abc import ABCMeta, abstractmethod

from referee.config import RefereeConfig
from referee.gamestage import Stage


class AbstractGameStateStore(metaclass=ABCMeta):
    @abstractmethod
    def get_state(self):
        raise NotImplementedError()

    @abstractmethod
    def get_matches(self, stage):
        raise NotImplementedError()

    @abstractmethod
    def get_match(self, stage, game_id):
        raise NotImplementedError()

    @abstractmethod
    def build_group_game(self):
        raise NotImplementedError()

    @abstractmethod
    def get_total_players(self):
        raise NotImplementedError()

    @abstractmethod
    def get_current_attacker_name(self, game_id, stage):
        raise NotImplementedError()

    @abstractmethod
    def get_current_opponent_name(self, game_id, stage):
        raise NotImplementedError()

    @abstractmethod
    def incr_score(self, stage, game_id, player_name):
        raise NotImplementedError()

    @abstractmethod
    def declare_winner(self, stage, game_id, player_name):
        raise NotImplementedError()

    @abstractmethod
    def is_match_won(self, stage, game_id, player_name):
        raise NotImplementedError()

    @abstractmethod
    def is_stage_game_completed(self, stage):
        raise NotImplementedError()

    @abstractmethod
    def switch_role(self, stage, game_id):
        raise NotImplementedError()

    @abstractmethod
    def get_game_winners(self):
        raise NotImplementedError()

    @abstractmethod
    def build_semi_final_game(self):
        raise NotImplementedError()

    @abstractmethod
    def reset(self):
        raise NotImplementedError()

    @staticmethod
    def get_game_state_store(store_cfg):
        stype, sconfig = [(k, v) for k, v in store_cfg.items()][0]
        return {"memory": lambda x: InmemoryGameState()}[stype](sconfig)


class InmemoryGameState(AbstractGameStateStore):
    def __init__(self) -> None:
        self.reset()
        self.config = RefereeConfig.instance()
        self.players = self.config.get_players()
        self.winning_score = self.config.get_winning_score()

    def get_state(self):
        return self.state

    def get_matches(self, stage):
        return {match["game-id"]: match for _, match in self.state[stage].items()}

    def get_match(self, stage, game_id):
        match = self.state[stage][game_id]
        return match if match.get("winner") is None else None

    def get_group(self, game_id):
        for group_name, data in self.state.items():
            if data.get(game_id, None):
                return group_name

    def build_group_game(self):
        total_players = self.get_total_players()
        start = 0
        players_name_list = list(self.players.keys())
        while start < total_players:
            game_id = uuid.uuid4().hex
            self.state[Stage.GROUP.name][game_id] = {
                "opponent": players_name_list[start + 1],
                "attacker": players_name_list[start],
                "game-id": game_id,
                "winner": None,
                players_name_list[start + 1]: 0,
                players_name_list[start]: 0,
            }
            start += 2

    def get_total_players(self):
        return len(self.players)

    def get_current_attacker_name(self, game_id, stage):
        return self.state[stage][game_id]["attacker"]

    def get_current_opponent_name(self, game_id, stage):
        return self.state[stage][game_id]["opponent"]

    def incr_score(self, stage, game_id, player_name):
        self.state[stage][game_id][player_name] = (
            self.state[stage][game_id].get(player_name, 0) + 1
        )

    def declare_winner(self, stage, game_id, player_name):
        self.state[stage][game_id]["winner"] = player_name

    def is_match_won(self, stage, game_id, player_name):
        try:
            return self.state[stage][game_id][player_name] == 5
        except KeyError:
            return False

    def is_stage_game_completed(self, stage):
        for winner in self.get_winners_name(stage):
            if not winner:
                return False
        return True

    def switch_role(self, stage, game_id):
        (
            self.state[stage][game_id]["attacker"],
            self.state[stage][game_id]["opponent"],
        ) = (
            self.state[stage][game_id]["opponent"],
            self.state[stage][game_id]["attacker"],
        )

    def get_game_winners(self, stage):
        result = {}
        for winner in self.get_winners_name(stage):
            result[winner] = self.players[winner]
        return result

    def get_winners_name(self, stage):
        games = self.state[stage]
        winners = []
        for _, game_details in games.items():
            if game_details["winner"]:
                winners.append(game_details["winner"])
        return winners

    def build_semi_final_game(self):
        group_winners = self.get_game_winners(Stage.GROUP.name)
        total_players = len(group_winners)
        start = 0
        players_name_list = list(group_winners.keys())
        while start < total_players:
            game_id = uuid.uuid4().hex
            self.state[Stage.SEMI.name][game_id] = {
                "opponent": players_name_list[start + 1],
                "attacker": players_name_list[start],
                "game-id": game_id,
                "winner": None,
                players_name_list[start + 1]: 0,
                players_name_list[start]: 0,
            }
            start += 2

    def build_final_game(self):
        semi_winners = self.get_game_winners(Stage.SEMI.name)
        total_players = len(semi_winners)
        start = 0
        players_name_list = list(semi_winners.keys())
        while start < total_players:
            game_id = uuid.uuid4().hex
            self.state[Stage.FINAL.name][game_id] = {
                "opponent": players_name_list[start + 1],
                "attacker": players_name_list[start],
                "game-id": game_id,
                "winner": None,
                players_name_list[start + 1]: 0,
                players_name_list[start]: 0,
            }
            start += 2

    def reset(self):
        self.state = defaultdict(dict)
