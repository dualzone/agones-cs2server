import requests
import definitions.agonesInfoResponse as AgonesInfoResponse

class AgonesManager:
    def __init__(self, url: str, port: int):
        self.__url = "http://" + url + ":" + str(port)

    def send_health_check(self) -> None:
        response = requests.post(self.__url + "/health")
        if response.status_code == 200:
            return
        else:
            raise Exception(f"Error fetching data: {response.status_code}")

    def send_ready(self) -> None:
        response = requests.post(self.__url + "/ready")
        if response.status_code == 200:
            return
        else:
            raise Exception(f"Error fetching data: {response.status_code}")

    def send_allocate(self) -> None:
        response = requests.post(self.__url + "/allocate")
        if response.status_code == 200:
            return
        else:
            raise Exception(f"Error fetching data: {response.status_code}")

    def send_shutdown(self) -> None:
        response = requests.post(self.__url + "/shutdown")
        if response.status_code == 200:
            return
        else:
            raise Exception(f"Error fetching data: {response.status_code}")

    def get_info(self) ->  AgonesInfoResponse:
        response = requests.get(self.__url + "/health")
        if response.status_code == 200:
            # Parse the response JSON into the JsonObject class
            data = response.json()
            obj = AgonesInfoResponse.from_dict(data)
            return obj
        else:
            raise Exception(f"Error fetching data: {response.status_code}")