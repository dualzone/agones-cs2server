# Étape 1 : Compiler le projet C# (build stage)
FROM mcr.microsoft.com/dotnet/sdk:8.0-bookworm-slim AS build
WORKDIR /app

# Copier le code source C# dans le conteneur
COPY WebApplication1/ ./src/

# Compiler l'application C#
RUN dotnet publish ./src -c Release -o /out --self-contained -r linux-x64

# Étape 2 : Créer l'image de base et configurer l'environnement

FROM steamcmd/steamcmd:ubuntu-22 as cppdeps

ENV USER root
ENV HOME /root/installer

# Set working directory
WORKDIR $HOME

RUN apt-get update \
 && apt-get install -y --no-install-recommends curl tar

# Donload and unpack installer
RUN curl http://media.steampowered.com/installer/steamcmd_linux.tar.gz \
    --output steamcmd.tar.gz --silent
RUN tar -xvzf steamcmd.tar.gz && rm steamcmd.tar.gz

FROM alpine:latest as build_stage

CMD ["bash"]

ARG PUID=1000
ENV USER=steam \
    HOMEDIR=/home/steam \
    STEAMCMDDIR=/home/steam/steamcmd

# Installer les dépendances et configurer les locales
RUN apk update && \
    apk add --no-interactive --upgrade \
    ca-certificates \
    net-tools \
    wget \
    unzip \
    bash \
    curl \
    jq \
    aspnetcore8-runtime  \
    dotnet8-runtime \
    dos2unix  &&\
    apk cache clean && \
    adduser -u "${PUID}" -D "${USER}" && \
    rm -rf /var/cache/apk/*
    #sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    #dpkg-reconfigure --frontend=noninteractive locales

# Définir les variables d'environnement pour les locales
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8


FROM build_stage AS dualzone-cs2server

# Définir le répertoire de travail pour SteamCMD et le serveur
WORKDIR "${HOMEDIR}"

COPY --from=cppdeps /etc/ssl/certs /etc/ssl/certs
COPY --from=cppdeps /lib/i386-linux-gnu /lib/
COPY --from=cppdeps "/root/installer/linux32/libstdc++.so.6" /lib/

COPY --from=build /out "${HOMEDIR}/cs2app"
COPY entrypoint.sh "${HOMEDIR}/entrypoint.sh"


RUN  set -x && \
    mkdir -p /root/Steam && \
    mkdir -p "${HOMEDIR}/cs2server" "${HOMEDIR}/.steam/sdk64" "${HOMEDIR}/.steam/sdk32" "${STEAMCMDDIR}/linux32" "${STEAMCMDDIR}/linux64" && \
    chown -R "${USER}:${USER}" "${HOMEDIR}" "${STEAMCMDDIR}" && \
    chmod -R 770 "${HOMEDIR}" "${STEAMCMDDIR}" && \
    chmod +x "${HOMEDIR}/cs2app/WebApplication1.dll" "${HOMEDIR}/entrypoint.sh" && \
    dos2unix "${HOMEDIR}/entrypoint.sh"

# Repasser à l’utilisateur non-root pour exécuter SteamCMD et le serveur
USER steam

# Exposer le port du serveur (par défaut 27015)
EXPOSE 27015/udp
EXPOSE 27015/tcp

# Démarrer le serveur CS2 via le script d'entrée
CMD ["sh","./entrypoint.sh"]
