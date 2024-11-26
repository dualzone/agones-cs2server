#!/bin/bash
set -e
echo "Installation du steam CMD"

curl -fsSL 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz' | tar xvzf - -C "${STEAMCMDDIR}"
chmod +x "${STEAMCMDDIR}/steamcmd.sh"
chmod +x "${STEAMCMDDIR}/linux32/steamcmd"
bash "${STEAMCMDDIR}/steamcmd.sh" +quit

echo "Create steamCMD links"
ln -s "${STEAMCMDDIR}/linux32/steamclient.so" "${STEAMCMDDIR}/steamservice.so"
ln -s "${STEAMCMDDIR}/linux32/steamclient.so" "${HOMEDIR}/.steam/sdk32/steamclient.so"
ln -s "${STEAMCMDDIR}/linux32/steamcmd" "${STEAMCMDDIR}/linux32/steam"
ln -s "${STEAMCMDDIR}/linux64/steamclient.so" "${HOMEDIR}/.steam/sdk64/steamclient.so"
ln -s "${STEAMCMDDIR}/linux64/steamcmd" "${STEAMCMDDIR}/linux64/steam"
ln -s "${STEAMCMDDIR}/steamcmd.sh" "${STEAMCMDDIR}/steam.sh"
ln -s "${STEAMCMDDIR}/linux64/steamclient.so" "/usr/lib/x86_64-linux-gnu/steamclient.so"
chmod +x "${STEAMCMDDIR}/steamcmd.sh"

wait

# Télécharger et mettre à jour le serveur CS2
echo "Téléchargement et mise à jour du serveur CS2 avec SteamCMD..."
bash "${STEAMCMDDIR}/steamcmd.sh" +force_install_dir "${HOMEDIR}/cs2server" +login anonymous +app_update 730 validate +quit

wait

if ! [[ -f "${HOMEDIR}/cs2server/game/bin/linuxsteamrt64/cs2" ]]; then
   echo "Erreur : le fichier cs2 n'a pas été trouvé dans le répertoire du serveur."
   exit 1
fi

echo "Install js deps"
cd "${HOMEDIR}/ServerManager"
npm install

chmod +x "${HOMEDIR}/cs2server/game/bin/linuxsteamrt64/cs2"
node app.js

