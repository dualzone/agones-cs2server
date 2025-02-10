import logging
import threading

from utils.envManager import EnvManager
import redis

class RedisClient:
    def __init__(self):
        self.__host = EnvManager.get_env_var("REDIS_HOST")
        self.__port = EnvManager.get_env_var("REDIS_PORT")
        self.__db = EnvManager.get_env_var("REDIS_DB", 10)
        self.__password = EnvManager.get_env_var("REDIS_PASSWORD")
        self.__client: RedisClient | None = None
        self._connect()

    def _connect(self):
        """Connect to the Redis server"""
        try:
            self.__client = redis.StrictRedis(
                host=self.__host,
                port=self.__port,
                db=self.__db,
                password=self.__password
            )
            self.__client.ping()
            logging.info("Connected to Redis")
        except redis.exceptions.ConnectionError:
            logging.error("Could not connect to Redis")
            raise Exception("Could not connect to Redis")

    def get_client(self):
        return self.__client

    def close(self):
        if self.__client:
            self.__client.connection_pool.disconnect()
            logging.info("Redis connection closed")

    def listen_for_events(self, channel, callback) -> threading.Thread:
        if not self.__client:
            raise Exception("Redis client not connected")
        print("Test  0")
        pubsub = self.__client.pubsub()
        pubsub.subscribe(channel)
        print("Test  1")
        return threading.Thread(target=self.__listen, args=(pubsub, callback), daemon=True)


    @staticmethod
    def __listen(pubsub, callback):
        for message in pubsub.listen():
            if message['type'] == 'message':
                callback(message['data'].decode('utf-8'))

    def publish_event(self, channel, message):
        if not self.__client:
            raise Exception("Redis client not connected")
        try:
            self.__client.publish(channel, message)
        except redis.exceptions.ConnectionError:
            logging.error("Could not publish message to Redis")
            raise Exception("Could not publish message to Redis")