from utils.redis.redisClient import RedisClient
from utils.agonesManager import AgonesManager
import utils.definitions.agonesResponseDef as AgonesInfoResponse

class ManagerHelper:
    def __init__(self, server_uuid: str):
        self.__redis_client: RedisClient = RedisClient()
        self.__agones: AgonesManager = AgonesManager('localhost', 9358)
        self.__server_id = server_uuid

    def set_server_ready(self):
        self.__agones.send_ready()
        self.__redis_client.publish_event('gameserver:register', self.__server_id)
        self.__redis_client.get_client().hset("gameserver:status", self.__server_id, "ready")

    def set_server_shutdown(self):
        self.__redis_client.get_client().hdel("gameserver:status", self.__server_id)
        self.__agones.send_shutdown()

    def set_server_allocated(self):
        self.__redis_client.get_client().hset("gameserver:status", self.__server_id, "allocated")
        self.__agones.send_allocate()
        print(self.__agones.get_info())
        #self.__redis_client.get_client().hset("gameserver:port", self.__server_id, )
        self.__parse_redis_config()

    def __parse_redis_config(self):
        """Here we parse redis config if error we raise exception and send event and wait for new config, if success we return the config"""
        pass