# DualZone

Installation de [Docker](https://www.docker.com/) 

Construction de l'image Docker

````shell
docker build -t cs2server .
````

Lancement de l'image
````shell
docker run -it -v cs2_data:/home/cs2user --network dns-net -p 27015/udp -p 27015/udp  cs2server
````
