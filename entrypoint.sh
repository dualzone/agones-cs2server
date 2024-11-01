#!/bin/bash

# Répertoire d'installation du serveur
SERVER_DIR="/home/cs2user/cs2_server"

# Vérifier si le serveur est déjà installé
if [ ! -d "$SERVER_DIR" ]; then
    echo "Téléchargement du serveur CS2..."
    ./steamcmd.sh +login anonymous +force_install_dir "$SERVER_DIR" +app_update 740 validate +quit
fi

# Démarrer le serveur CS2
echo "Démarrage du serveur CS2..."
# Ajoutez ici la commande pour démarrer le serveur CS2
# Exemple : cd $SERVER_DIR && ./srcds_run -game cs2 -console -maxplayers 16

# Exécuter l'application .NET
echo "Démarrage de l'application C#..."
exec /home/cs2user/cs2_app/WebApplication
