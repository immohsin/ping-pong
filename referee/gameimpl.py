import json

from referee.gamestage import Stage


class GameImpl:
    def __init__(self, pubsub, game_state, logger) -> None:
        self.pubsub = pubsub
        self.game_state = game_state
        self.logger = logger
        self.qualifiers = {
            Stage.GROUP.name: 4,
            Stage.SEMI.name: 2,
            Stage.FINAL.name: 1,
        }

    def add_match_end_listener(self, semi_final_fn, final_fn, send_report_fn):
        self.listeners = {
            Stage.GROUP.name: semi_final_fn,
            Stage.SEMI.name: final_fn,
            Stage.FINAL.name: send_report_fn,
        }

    def send_instruction_2_all(self, stage):
        matches = self.game_state.get_matches(stage)
        for _, instructions in matches.items():
            self.pubsub.publish(
                instructions["attacker"],
                json.dumps({"msg_type": "instruction", **instructions}),
            )

    def send_instruction(self, stage, game_id):
        match = self.game_state.get_match(stage, game_id)
        if match:
            self.pubsub.publish(
                match["attacker"], json.dumps({"msg_type": "instruction", **match})
            )
        else:
            if len(self.game_state.get_winners_name(stage)) == self.qualifiers[stage]:
                self.listeners[stage]()

    def process_defence(self, stage, game_id, defended):
        opponent = self.game_state.get_current_opponent_name(game_id, stage)
        attacker = self.game_state.get_current_attacker_name(game_id, stage)
        if defended == "True":
            self.game_state.incr_score(stage, game_id, opponent)
            self.game_state.switch_role(stage, game_id)
            if self.game_state.is_match_won(stage, game_id, opponent):
                self.game_state.declare_winner(stage, game_id, opponent)
        else:
            self.game_state.incr_score(stage, game_id, attacker)
            if self.game_state.is_match_won(stage, game_id, attacker):
                self.game_state.declare_winner(stage, game_id, attacker)
        self.send_instruction(stage, game_id)

    def process_attack(self, guessed_number, opponent, game_id):
        self.pubsub.publish(
            opponent,
            json.dumps(
                {
                    "msg_type": "attack",
                    "guessed_number": guessed_number,
                    "game-id": game_id,
                }
            ),
        )
