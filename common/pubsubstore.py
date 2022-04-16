from abc import ABCMeta, abstractmethod

import redis


class AbstractPubsubStore(metaclass=ABCMeta):
    @abstractmethod
    def init(self):
        raise NotImplementedError()

    @abstractmethod
    def publish(self, channel, data):
        raise NotImplementedError()

    @abstractmethod
    def subscribe(self, channel):
        raise NotImplementedError()

    @abstractmethod
    def get_data(self):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()

    @staticmethod
    def get_pubsub_store(store_cfg):
        pubsub_type, pubsub_config = [(k, v) for k, v in store_cfg.items()][0]
        return {"redis": lambda x: RedisPubsubStore(x)}[pubsub_type](pubsub_config)


class RedisPubsubStore:
    def __init__(self, store_config) -> None:
        self.host = store_config["host"]
        self.port = store_config["port"]
        self.init()

    def init(self):
        self.redis = redis.StrictRedis(
            self.host, self.port, charset="utf-8", decode_responses=True
        )
        self.subscriber = self.redis.pubsub()

    def publish(self, channel, data):
        self.redis.publish(channel, data)

    def subscribe(self, channel):
        self.subscriber.subscribe(**channel)

    # Sync API
    def get_data(self):
        for message in self.subscriber.listen():
            yield message

    # Async API
    def run_in_background(self, sleep_time=0.001):
        try:
            thread = self.subscriber.run_in_thread(sleep_time=sleep_time, daemon=True)
        except Exception as e:
            print(str(e))
        return thread

    def close(self):
        self.subscriber.unsubscribe()
        self.redis.close()
