# DualZone

Installation de [Docker](https://www.docker.com/) 

Construction de l'image Docker

````shell
docker build -t cs2server .
````

Lancement de l'image
````shell
docker run -it -v cs2_data:/home/cs2user/cs2_server -p 27015/udp -p 27015/udp -e CS2_STEAM_TOKEN=ECE2CDBA46245CD80E318A1449A8CBA4 -e CS2_RCON_PASSWORD=123456  cs2server
````


