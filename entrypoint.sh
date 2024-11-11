#!/bin/bash

# Première exécution de SteamCMD pour télécharger les mises à jour du runtime Steam
/home/cs2user/Steam/steamcmd.sh +quit

# Télécharger et mettre à jour le serveur CS2
echo "Téléchargement et mise à jour du serveur CS2 avec SteamCMD..."
/home/cs2user/Steam/steamcmd.sh +force_install_dir /home/cs2user/cs2_server +login anonymous +app_update 730 validate +quit



# Vérifier que le fichier cs2.sh existe avant de lancer
if [ -f /home/cs2user/cs2_server/game/bin/linuxsteamrt64/cs2 ]; then
    echo "Le script cs2.sh est trouvé, démarrage du serveur..."
    dotnet /home/cs2user/cs2_app/WebApplication1.dll
else
    echo "Erreur : le fichier cs2.sh n'a pas été trouvé dans le répertoire du serveur."
    exit 1
fi

