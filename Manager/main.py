import multiprocessing
import os
import threading
from time import sleep

from utils.envManager import EnvManager
from manager import serverManger
from utils.agonesManager import AgonesManager
from utils.redis.redisClient import RedisClient
import asyncio

running: bool = True

def main():
    EnvManager.get_env_var("TEST")
    print("Hello, World!")
    print("Launching server...")
    agones = AgonesManager('localhost', 9358)
    health_thread =  multiprocessing.Process(target=send_health_check, daemon=True)
    health_thread.start()
    server = serverManger.ServerManager(EnvManager.get_env_var("CS2_STEAM_TOKEN"), EnvManager.get_env_var("CS2_RCON_PASSWORD"), "")
    agones.send_ready()
    server.wait_for_server_exit()
    health_thread.terminate()

def send_health_check():
    while running:
        print("Sending health check")
        agones = AgonesManager('localhost', 9358)
        agones.send_health_check()  # Call the health check function
        print("Health check sent")
        sleep(10)

if __name__ == "__main__":
    main()
