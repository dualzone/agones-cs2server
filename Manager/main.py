import multiprocessing
import os
import threading
from time import sleep
from fastapi import FastAPI
import uvicorn

from manager.scanConfig import ScanConfig
from utils.configureCS2Modding import ConfigureCS2Modding
from utils.configureLan import ConfigureLan
from utils.envManager import EnvManager
from manager import serverManger
from utils.agonesManager import AgonesManager
from utils.definitions.serverConfig import Game
from utils.redis.redisClient import RedisClient
import asyncio

running: bool = True
app = FastAPI()

def main():

    print("Configuration du modding sur CS2")
    lanConfig: ConfigureLan = ConfigureLan()
    lanConfig.write_config()
    configurator: ConfigureCS2Modding = ConfigureCS2Modding()
    configurator.ensure_modding_line()

    sleep(10)


    print("Launching Health check...")
    agones = AgonesManager(EnvManager.get_env_var("AGONES_HOST", "127.0.0.1"), 9358)
    health_thread =  multiprocessing.Process(target=send_health_check, daemon=True)
    health_thread.start()

    print("Launching FastAPI...")
    api_thread =  multiprocessing.Process(target=start_api, daemon=True)
    api_thread.start()

    print("Launching CS2 Server...")
    server = serverManger.ServerManager(EnvManager.get_env_var("CS2_STEAM_TOKEN"), EnvManager.get_env_var("CS2_RCON_PASSWORD"), "")
    agones.send_ready()
    server.wait_for_server_exit()
    health_thread.terminate()
    api_thread.terminate()

def send_health_check():
    while running:
        agones = AgonesManager(EnvManager.get_env_var("AGONES_HOST", "127.0.0.1"), 9358)
        agones.send_health_check()  # Call the health check function
        sleep(10)

def start_api():
    uvicorn.run(app, host="0.0.0.0", port=8081)

@app.get("/config/{server_id}")
def read_root(server_id: str):
    print(f"Getting config for server {server_id}")
    game: Game = ScanConfig(server_id).get_game_instance()
    return  game.to_dict()

@app.get("/events/{server_id}")
def read_root(server_id: str):
    print("Events")
    return ""

@app.get("/eventula/{server_id}")
def read_root(server_id: str):
    print("eventula")
    return ""



if __name__ == "__main__":
    main()
