import csv

from common.pubsubstore import AbstractPubsubStore

from referee.gameimpl import GameImpl
from referee.gamestate import AbstractGameStateStore
from referee.gamestage import Stage


class RefereeSever:
    def __init__(self, config, logger) -> None:
        self.config = config
        self.logger = logger
        self.total_player_joined = set()
        self.game_state = AbstractGameStateStore.get_game_state_store(
            self.config.get_game_state_store()
        )

    def start(self):
        self.pubsub = AbstractPubsubStore.get_pubsub_store(self.config.get_pubstore())
        self.game_impl = GameImpl(self.pubsub, self.game_state, self.logger)
        self.game_impl.add_match_end_listener(
            self.start_semi_final, self.start_final, self.send_report
        )
        self.game_state.build_group_game()

    def stop(self):
        self.pubsub.close()

    def process_attack_request(self, guessed_number, opponent, game_id):
        self.game_impl.process_attack(guessed_number, opponent, game_id)

    def process_defence_request(self, game_id, defended):
        stage = self.game_state.get_group(game_id)

        self.game_impl.process_defence(stage, game_id, defended)

    def start_group_game(self):
        self.logger.info("Group games started!")
        self.game_impl.send_instruction_2_all(Stage.GROUP.name)

    def start_semi_final(self):
        self.game_state.build_semi_final_game()
        self.logger.info("Semi finals started!")
        self.game_impl.send_instruction_2_all(Stage.SEMI.name)

    def start_final(self):
        self.game_state.build_final_game()
        self.logger.info("Final started!")
        self.game_impl.send_instruction_2_all(Stage.FINAL.name)

    def notify_player_joining(self, player_name):
        self.total_player_joined.add(player_name)
        self.logger.info(f"{player_name} joined the championship game!")
        if len(self.total_player_joined) == self.game_state.get_total_players():
            self.start_group_game()

    def start_championship(self):
        self.logger.info("Championship started")
        self.game_state.build_group_game()
        self.start_group_game()

    def send_report(self):
        self.logger.info("Generating match report...")
        fields = [
            "stage",
            "player1",
            "player2",
            "game-id",
            "winner",
            "player1_score",
            "player2_score",
        ]
        data = []
        for stage, d in self.game_state.get_state().items():
            for _, report_data in d.items():
                data.append({"stage": stage, **report_data})

        with open("report/championship_report.csv", "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            for d in data:
                writer.writerow(
                    {
                        "stage": d["stage"],
                        "player1": d["attacker"],
                        "player2": d["opponent"],
                        "game-id": d["game-id"],
                        "winner": d["winner"],
                        "player1_score": d[d["attacker"]],
                        "player2_score": d[d["opponent"]],
                    }
                )
        self.game_state.reset()
