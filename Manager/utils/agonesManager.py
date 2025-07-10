import requests
import utils.definitions.agonesResponseDef as AgonesInfoResponse

class AgonesManager:
    def __init__(self, url: str, port: int):
        self.__url = "http://" + url + ":" + str(port)
        self.__headers = {'Content-type': 'application/json'}

    def send_health_check(self) -> None:
        pass

    def send_ready(self) -> None:
        pass

    def send_allocate(self) -> None:
        pass

    def send_shutdown(self) -> None:
        pass

    def get_info(self):
        pass
