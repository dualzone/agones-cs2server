import requests
import utils.definitions.agonesResponseDef as AgonesInfoResponse

class AgonesManager:
    def __init__(self, url: str, port: int):
        self.__url = "http://" + url + ":" + str(port)
        self.__headers = {'Content-type': 'application/json'}

    def send_health_check(self) -> None:
        response = requests.post(self.__url + "/health", headers=self.__headers, json={})
        if response.status_code == 200:
            return
        else:
            raise Exception(f"Error fetching data: {response.status_code}")

    def send_ready(self) -> None:
        response = requests.post(self.__url + "/ready", headers=self.__headers, json={})
        if response.status_code == 200:
            return
        else:
            raise Exception(f"Error fetching data: {response.status_code}")

    def send_allocate(self) -> None:
        response = requests.post(self.__url + "/allocate", headers=self.__headers, json={})
        if response.status_code == 200:
            return
        else:
            raise Exception(f"Error fetching data: {response.status_code}")

    def send_shutdown(self) -> None:
        response = requests.post(self.__url + "/shutdown", headers=self.__headers, json={})
        if response.status_code == 200:
            return
        else:
            raise Exception(f"Error fetching data: {response.status_code}")

    def get_info(self):
        response = requests.get(self.__url + "/gameserver", headers=self.__headers)
        if response.status_code == 200:
            # Parse the response JSON into the JsonObject class
            return response.json()
        else:
            raise Exception(f"Error fetching data: {response.status_code}")