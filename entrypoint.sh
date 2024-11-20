#!/bin/bash

mkdir -p "${STEAMAPPDIR}" || true

# Première exécution de SteamCMD pour télécharger les mises à jour du runtime Steam
bash "${STEAMCMDDIR}/steamcmd.sh" +quit

wait

# Télécharger et mettre à jour le serveur CS2
echo "Téléchargement et mise à jour du serveur CS2 avec SteamCMD..."
bash "${STEAMCMDDIR}/steamcmd.sh" +force_install_dir "${HOMEDIR}"/cs2_server +login anonymous +app_update 730 validate +quit

mkdir -p ~/.steam/sdk64
ln -sfT ${STEAMCMDDIR}/linux64/steamclient.so ~/.steam/sdk64/steamclient.so

# Vérifier que le fichier cs2.sh existe avant de lancer
if ! [[ -f "${HOMEDIR}/cs2server/game/bin/linuxsteamrt64/cs2" ]]; then
    echo "Erreur : le fichier cs2 n'a pas été trouvé dans le répertoire du serveur."
    exit 1
fi



chmod +x "${HOMEDIR}/cs2server/game/bin/linuxsteamrt64/cs2"
dotnet /home/cs2user/cs2app/WebApplication1.dll || exit 1

