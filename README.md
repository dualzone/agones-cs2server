# DualZone

Installation de [Docker](https://www.docker.com/) 

Construction de l'image Docker

````shell
docker build -t cs2server .
````

*Les deux images suivantes doivent être lancées en même temps*

Lancement de l'image
````shell
docker run -it -v cs2_data:/home/steam/cs2server --network=host --rm -p 27015/udp -p 27015/udp -e CS2_STEAM_TOKEN=ECE2CDBA46245CD80E318A1449A8CBA4 -e CS2_RCON_PASSWORD=123456 cs2server
````
Lancement du conteneur de dev agones

````shell
docker run --network=host --rm us-docker.pkg.dev/agones-images/release/agones-sdk:1.45.0 --local
````


