#!/bin/bash
cd /home/cs2user/

echo "Démarrage de l'entrypoint..."

# Vérification des permissions du répertoire du serveur
echo "Vérification des permissions..."
ls -l /home/cs2user/steamcmd.sh
ls -l /home/cs2user/linux32/

# Télécharger et mettre à jour le serveur CS2
echo "Téléchargement et mise à jour du serveur CS2 avec SteamCMD..."
./steamcmd.sh +login anonymous +force_install_dir /home/cs2user/cs2_server +app_update 730 validate +quit

# Vérifier l'état du répertoire du serveur
echo "Répertoire du serveur CS2 :"
ls -l /home/cs2user/cs2_server

# Démarrer le serveur CS2
echo "Démarrage du serveur CS2..."
dotnet /home/cs2user/cs2_app/WebApplication1.dll
