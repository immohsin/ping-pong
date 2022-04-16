import json

from common.pubsubstore import AbstractPubsubStore

from player.playerimpl import PlayerImpl


class PlayerSever:
    def __init__(self, config, logger) -> None:
        self.config = config
        self.logger = logger
        self.player_impl = PlayerImpl(config, logger)

    def start(self):
        self.pubsub = AbstractPubsubStore.get_pubsub_store(self.config.get_pubstore())
        self.pubsub.subscribe(
            {self.config.get_player_name(): self.handle_async_pubsub_message}
        )
        self.player_impl.join_championship()
        self.thread = self.pubsub.run_in_background()

    def stop(self):
        self.pubsub.close()
        self.thread.stop()

    def handle_async_pubsub_message(self, message):
        if message["data"] and message["type"] != "subscribe":
            data = json.loads(message["data"])
            if data["msg_type"] == "instruction":
                self.player_impl.read_game_instructions(data)
            if data["msg_type"] == "attack":
                self.player_impl.defend_number(data)
