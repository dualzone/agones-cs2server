FROM python:3.13-slim-bookworm as build_stage


ARG PUID=1100
ENV USER=steam \
    HOMEDIR=/home/steam \
    STEAMCMDDIR=/home/steam/steamcmd

# Installer les dépendances et configurer les locales
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y \
    ca-certificates \
    net-tools \
    wget \
    unzip \
    lib32stdc++6  \
     gcc-multilib \
    lib32gcc-s1 \
    jq \
    locales \
    locales-all \
    curl &&\
    useradd -u "${PUID}" -m "${USER}" && \
    rm -rf /var/lib/apt/lists/* && \
    apt clean && \
    localedef -i en_US -f UTF-8 en_US.UTF-8 && \
    echo "LANG=en_US.UTF-8" > /etc/locale.conf && \
    echo "LC_ALL=en_US.UTF-8" >> /etc/environment

# Définir les variables d'environnement pour les locales
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8


FROM build_stage AS dualzone-cs2server

# Définir le répertoire de travail pour SteamCMD et le serveur
WORKDIR "${HOMEDIR}"

COPY ./Manager "${HOMEDIR}/Manager"
COPY entrypoint.sh "${HOMEDIR}/entrypoint.sh"


RUN  set -x && \
    mkdir -p /root/Steam && \
    mkdir -p "${HOMEDIR}/cs2server" "${HOMEDIR}/.steam/sdk64" "${HOMEDIR}/.steam/sdk32" "${STEAMCMDDIR}/linux32" "${STEAMCMDDIR}/linux64" && \
    chown -R "${USER}:${USER}" "${HOMEDIR}" "${STEAMCMDDIR}" "/usr/lib/x86_64-linux-gnu" && \
    chmod -R 770 "${HOMEDIR}" "${STEAMCMDDIR}" "/usr/lib/x86_64-linux-gnu" && \
    chmod +x "${HOMEDIR}/entrypoint.sh"

# Repasser à l’utilisateur non-root pour exécuter SteamCMD et le serveur
USER steam

# Exposer le port du serveur (par défaut 27015)
EXPOSE 27015/udp
EXPOSE 27015/tcp

# Démarrer le serveur CS2 via le script d'entrée
CMD ["sh","./entrypoint.sh"]
