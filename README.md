# DualZone

Installation de [Docker](https://www.docker.com/) 

Construction de l'image Docker

````shell
docker build -t cs2server .
````
Lancement de l'image
````shell
docker run -it -v cs2_data:/home/cs2user cs2server
````
