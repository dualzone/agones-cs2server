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
#bash "${STEAMCMDDIR}/steamcmd.sh" +force_install_dir "${HOMEDIR}/cs2server" +login anonymous +app_update 730 validate +quit

wait

echo "Installation des gt5 et de ses dépendances"
mkdir "${HOMEDIR}/Downloads"
wget https://mms.alliedmods.net/mmsdrop/2.0/mmsource-2.0.0-git1319-linux.tar.gz -O "${HOMEDIR}/Downloads/mmsource.linux.tar.gz"
wget https://sm.alliedmods.net/smdrop/1.13/sourcemod-1.13.0-git7199-linux.tar.gz -O "${HOMEDIR}/Downloads/sourcemod.linux.tar.gz"
wget https://github.com/splewis/get5/releases/download/v0.15.0/get5-v0.15.0.tar.gz -O "${HOMEDIR}/Downloads/get5.linux.tar.gz"
wget https://github.com/hexa-core-eu/SteamWorks/releases/download/v1.2.4/package-linux.zip  -O "${HOMEDIR}/Downloads/steamworks.zip"

tar -xzf "${HOMEDIR}/Downloads/mmsource.linux.tar.gz" -C "${HOMEDIR}/cs2server/game/csgo" --overwrite
tar -xzf  "${HOMEDIR}/Downloads/sourcemod.linux.tar.gz" -C "${HOMEDIR}/cs2server/game/csgo" --overwrite
tar -xzf  "${HOMEDIR}/Downloads/get5.linux.tar.gz" -C "${HOMEDIR}/cs2server/game/csgo" --overwrite
unzip -o "${HOMEDIR}/Downloads/steamworks.zip" -d "${HOMEDIR}/cs2server/game/csgo"

echo "Configuration de gameinfo.gi"
sed -i '/Game\s*csgo$/i \			Game   csgo/addons/metamod' /home/steam/cs2server/game/csgo/gameinfo.gi

echo "Installation des dépendances Python"
cd "${HOMEDIR}/Manager"
pip install -r requirements.txt

chmod +x "${HOMEDIR}/cs2server/game/bin/linuxsteamrt64/cs2"
python3 main.py

