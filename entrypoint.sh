#!/bin/bash

# Première exécution de SteamCMD pour télécharger les mises à jour du runtime Steam
/home/cs2user/Steam/steamcmd.sh +quit

# Télécharger et mettre à jour le serveur CS2
echo "Téléchargement et mise à jour du serveur CS2 avec SteamCMD..."
/home/cs2user/Steam/steamcmd.sh +force_install_dir /home/cs2user/cs2_server +login anonymous +app_update 730 validate +quit


# Vérifier que le fichier cs2.sh existe avant de lancer
if ! [[ -f /home/cs2user/cs2_server/game/bin/linuxsteamrt64/cs2 ]]; then
    echo "Erreur : le fichier cs2.sh n'a pas été trouvé dans le répertoire du serveur."
    exit 1
fi


#!/bin/bash
echo "Variables d'environnement :"
env

echo "Chemin d'accès :"
echo $PATH

echo "Contenu du répertoire de l'application :"
ls -l /home/cs2user/cs2_app

echo "Contenu du répertoire du serveur CS2 :"
ls -l /home/cs2user/cs2_server/game/bin/linuxsteamrt64

wait

sleep 5

dotnet /home/cs2user/cs2_app/WebApplication1.dll || exit 1

