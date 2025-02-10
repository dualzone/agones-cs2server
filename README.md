# DualZone

Installation de [Docker](https://www.docker.com/) 

Construction de l'image Docker

````shell
docker build -t cs2server .
````

Run l'environnement
````shell
docker network create local-dev
docker run -p 9357:9357 -p 9358:9358 -p 8080:8080 --rm --name agones --network local-dev -v $(pwd)\gameserver.yaml:/tmp/gameserver.yaml us-docker.pkg.dev/agones-images/release/agones-sdk:1.46.0 --local --address 0.0.0.0 -f /tmp/gameserver.yaml
docker run -it -v cs2_data:/home/steam/cs2server -p 27015:27015/tcp -p 27015:27015/udp --name cs2server --network local-dev --rm --env-file=.env cs2server
````



TODO:
- Ajout des novueau status
- Vérification de la la  ligne dans le gameinfo.gi
- Pool des event gt5