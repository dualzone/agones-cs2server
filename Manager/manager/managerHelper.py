from time import sleep

from utils.envManager import EnvManager
from utils.redis.redisClient import RedisClient
from utils.agonesManager import AgonesManager
import utils.definitions.agonesResponseDef as AgonesInfoResponse
from manager.scanConfig import ScanConfig
from utils.definitions.serverConfig import Game

class ManagerHelper:
    def __init__(self, server_uuid: str):
        self.__redis_client: RedisClient = RedisClient()
        self.__agones: AgonesManager = AgonesManager(EnvManager.get_env_var("AGONES_HOST", "127.0.0.1"), 9358)
        self.__server_id = server_uuid
        self.__config_error = 0

    def set_server_starting(self):
        self.__redis_client.publish_event('gameserver:register', self.__server_id)
        self.__redis_client.get_client().hset("gameserver:status", self.__server_id, "starting")

    def set_server_ready(self):
        self.__agones.send_ready()
        self.__redis_client.publish_event('gameserver:ready', self.__server_id)
        self.__redis_client.get_client().hset("gameserver:status", self.__server_id, "ready")

    def set_server_shutdown(self):
        self.__redis_client.get_client().hdel("gameserver:status", self.__server_id)
        self.__agones.send_shutdown()

    def set_server_allocated(self) -> Game:
        config: Game = self.__parse_redis_config()
        self.__agones.send_allocate()
        print(self.__agones.get_info())
        self.__redis_client.get_client().hset("gameserver:status", self.__server_id, "allocated")
        return config

    def __parse_redis_config(self) -> Game:
        scanner: ScanConfig = ScanConfig(self.__server_id)
        try:
            config: Game  = scanner.get_game_instance()
            self.__redis_client.publish_event("gameserver:configValidate", self.__server_id)
            print("Config parsed successfully")
            return config
        except ValueError as e:
            print("Error parsing config, retrying  in 10 seconds")
            self.__redis_client.publish_event("gameserver:configError", self.__server_id)
            print(e)
            sleep(10)
            return self.__parse_redis_config()
