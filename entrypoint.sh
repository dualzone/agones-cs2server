#!/bin/bash
cd /home/cs2user/

echo "Démarrage de l'entrypoint"

# Vérifier si le serveur est déjà installé
#./steamcmd.sh +login anonymous +force_install_dir "$SERVER_DIR" +app_update 740 validate +quit
steamcmd +login anonymous +force_install_dir /home/cs2user/cs2_server 
steamcmd +app_update 730 validate +quit

# Répertoire d'installation du serveur
SERVER_DIR="/home/cs2user/cs2_server"

# Démarrer le serveur CS2
echo "Démarrage du serveur CS2..."

# Exécuter l'application .NET
echo "Démarrage de l'application C#..."

dotnet /home/cs2user/cs2_app/WebApplication1.dll
