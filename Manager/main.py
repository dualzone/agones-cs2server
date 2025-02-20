
import multiprocessing
from time import sleep
import uvicorn
from manager.scanConfig import ScanConfig
from utils.configureCS2Modding import ConfigureCS2Modding
from utils.definitions.events import EventBase, SeriesStartEvent, MapResultEvent, SeriesEndEvent, SidePickedEvent, \
    MapPickedEvent, MapVetoedEvent, RoundEndEvent, MatchGoingLiveEvent
from utils.envManager import EnvManager
from manager import serverManger
from utils.agonesManager import AgonesManager
from utils.definitions.serverConfig import Game
from utils.redis.redisClient import RedisClient
from fastapi import FastAPI, Request, HTTPException
from typing import Dict, Type


running: bool = True
app = FastAPI()

def main():

    print("Configuration du modding sur CS2")
    configurator: ConfigureCS2Modding = ConfigureCS2Modding()
    configurator.ensure_modding_line()

    print("Launching Health check...")
    #agones = AgonesManager(EnvManager.get_env_var("AGONES_HOST", "127.0.0.1"), 9358)
    #health_thread =  multiprocessing.Process(target=send_health_check, daemon=True)
    #health_thread.start()

    print("Launching FastAPI...")
    api_thread =  multiprocessing.Process(target=start_api, daemon=True)
    api_thread.start()

    print("Launching CS2 Server...")
    server = serverManger.ServerManager(EnvManager.get_env_var("CS2_STEAM_TOKEN"), EnvManager.get_env_var("CS2_RCON_PASSWORD"), "")
    #agones.send_ready()
    server.wait_for_server_exit()
    #health_thread.terminate()
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

event_classes: Dict[str, Type[EventBase]] = {
    "series_start": SeriesStartEvent,
    "map_result": MapResultEvent,
    "series_end": SeriesEndEvent,
    "side_picked": SidePickedEvent,
    "map_picked": MapPickedEvent,
    "map_vetoed": MapVetoedEvent,
    "round_end": RoundEndEvent,
    "going_live": MatchGoingLiveEvent,
}

@app.post("/events/{server_id}")
async def read_root(server_id: str, request: Request):
    event_data = await request.json()
    redis_client: RedisClient = RedisClient()
    event_type = event_data.get("event")
    if not event_type or event_type not in event_classes:
        raise HTTPException(status_code=400, detail="Event type not supported")
    try:
        event_instance = event_classes[event_type](**event_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid event data: {str(e)}")
    json_data = event_instance.model_dump_json()
    redis_client.publish_event(f"gameserver:{server_id}:event", json_data)
    if event_instance.event == "map_result":
        redis_client.publish_event(f"gameserver:reset", server_id)



if __name__ == "__main__":
    main()
