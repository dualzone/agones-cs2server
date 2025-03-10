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
#
bash "${STEAMCMDDIR}/steamcmd.sh" +force_install_dir "${HOMEDIR}/cs2server" +login anonymous +app_update 730 validate +quit

wait

echo "Installation des gt5 et de ses dépendances"
mkdir "${HOMEDIR}/Downloads"
wget https://mms.alliedmods.net/mmsdrop/2.0/mmsource-2.0.0-git1319-linux.tar.gz -O "${HOMEDIR}/Downloads/mmsource.linux.tar.gz"
wget https://github.com/roflmuffin/CounterStrikeSharp/releases/download/v305/counterstrikesharp-with-runtime-build-305-linux-e99d27c.zip -O "${HOMEDIR}/Downloads/counterstrikesharp.zip"
wget https://github.com/shobhit-pathak/MatchZy/releases/download/0.8.8/MatchZy-0.8.8.zip -O "${HOMEDIR}/Downloads/MatchZy.zip"


tar -xzf "${HOMEDIR}/Downloads/mmsource.linux.tar.gz" -C "${HOMEDIR}/cs2server/game/csgo" --overwrite
unzip -o "${HOMEDIR}/Downloads/counterstrikesharp.zip" -d "${HOMEDIR}/cs2server/game/csgo"
unzip -o "${HOMEDIR}/Downloads/MatchZy.zip" -d "${HOMEDIR}/cs2server/game/csgo"

echo "Installation des dépendances Python"
cd "${HOMEDIR}/Manager"
pip install -r requirements.txt

wait

echo "Configuration de gameinfo.gi"
mv "${HOMEDIR}/gameinfo.gi.tmp" "${HOMEDIR}/cs2server/game/csgo/gameinfo.gi"

wait
mkdir -p /home/steam/cs2server/game/csgo/PugSharp/Config/
chmod +x "${HOMEDIR}/cs2server/game/bin/linuxsteamrt64/cs2"
python3 main.py