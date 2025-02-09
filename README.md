# DualZone

Installation de [Docker](https://www.docker.com/) 

Construction de l'image Docker

````shell
docker build -t cs2server .
````

Set les variables sous windows: 
```powershell

$env:CS2_STEAM_TOKEN="ECE2CDBA46245CD80E318A1449A8CBA4"
$env:CS2_RCON_PASSWORD="YOUR_RCON"
$env:REDIS_PASSWORD="dualzone"
$env:REDIS_HOST="127.0.0.1"
$env:REDIS_PORT="6379"
$env:HOME_DIR="D:\dualzone"



```

*Les deux images suivantes doivent être lancées en même temps*

Lancement de l'image
````shell
docker run -it -v cs2_data:/home/steam/cs2server --network=host --rm -p 27015/udp -p 27015/udp -e CS2_STEAM_TOKEN=ECE2CDBA46245CD80E318A1449A8CBA4 -e CS2_RCON_PASSWORD=123456 cs2server
````
Lancement du conteneur de dev agones

````shell
docker run --network=host --rm us-docker.pkg.dev/agones-images/release/agones-sdk:1.45.0 --local
````


