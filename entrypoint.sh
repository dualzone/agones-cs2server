#!/bin/bash

# Accéder au répertoire Steam et exécuter SteamCMD
cd /home/cs2user/Steam && ./steamcmd.sh +quit

echo "Démarrage de l'entrypoint..."

# Vérification des permissions du répertoire du serveur
echo "Vérification des permissions..."
ls -l /home/cs2user/Steam/steamcmd.sh

# Télécharger et mettre à jour le serveur CS2
echo "Téléchargement et mise à jour du serveur CS2 avec SteamCMD..."
/home/cs2user/Steam/steamcmd.sh +force_install_dir /home/cs2user/cs2_server +login anonymous +app_update 730 validate +quit

# Vérifier l'état du répertoire du serveur après l'installation
echo "Répertoire du serveur CS2 :"

# Vérifier que le fichier cs2.sh existe avant de lancer
if [ -f /home/cs2user/cs2_server/game/cs2.sh ]; then
    echo "Le script cs2.sh est trouvé, démarrage du serveur..."
else
    echo "Erreur : le fichier cs2.sh n'a pas été trouvé dans le répertoire du serveur."
    exit 1
fi

echo "Path du cs2.sh : $(pwd)/cs2.sh"
echo "Vérification des librairies Steam..."
ldd /home/cs2user/cs2_server/game/cs2.sh

# Démarrer le serveur CS2 dans l'environnement Steam
echo "Démarrage du serveur CS2 avec Steam pour Linux..."
cd /home/cs2user/cs2_server/game
./cs2.sh
