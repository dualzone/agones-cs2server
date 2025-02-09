import multiprocessing
import os
import threading
from time import sleep
from fastapi import FastAPI
import uvicorn

from manager.scanConfig import ScanConfig
from utils.envManager import EnvManager
from manager import serverManger
from utils.agonesManager import AgonesManager
from utils.redis.redisClient import RedisClient
import asyncio

running: bool = True
app = FastAPI()

def main():
    EnvManager.get_env_var("TEST")
    print("Hello, World!")

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
    return ScanConfig(server_id).to_json()



if __name__ == "__main__":
    main()
