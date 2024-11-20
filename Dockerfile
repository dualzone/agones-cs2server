# Étape 1 : Compiler le projet C# (build stage)
FROM mcr.microsoft.com/dotnet/sdk:8.0-bookworm-slim AS build
WORKDIR /app

# Copier le code source C# dans le conteneur
COPY WebApplication1/ ./src/

# Compiler l'application C#
RUN dotnet publish ./src -c Release -o /out

# Étape 2 : Créer l'image de base et configurer l'environnement

FROM cm2network/steamcmd:root-bookworm as build_stage

# Installer les dépendances et configurer les locales
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    locales \
    locales-all \
    net-tools \
    wget \
    lib32z1 \
    libicu-dev \
    unzip \
    jq \
    dnsutils \
    dos2unix  &&\
    localedef -i en_US -f UTF-8 en_US.UTF-8 && \
    apt-get clean &&\
    find /var/lib/apt/lists/ -type f -delete

# Définir les variables d'environnement pour les locales
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

RUN wget https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb -O packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    rm packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y  --no-install-recommends \
    aspnetcore-runtime-9.0 \
    dotnet-runtime-9.0


FROM build_stage AS dualzone-cs2server

# Créer un utilisateur non-root pour exécuter le serveur
RUN  set -x && \
    mkdir -p /root/Steam && \
    mkdir -p "${HOMEDIR}/cs2server" && \
    chown -R "${USER}:${USER}" "${HOMEDIR}" && \
    chmod -R 770 "${HOMEDIR}/cs2server"

# Définir le répertoire de travail pour SteamCMD et le serveur
WORKDIR "${HOMEDIR}"
# Copier l'exécutable C# depuis l'étape de compilation
COPY --from=build /out "${HOMEDIR}/cs2app"

# Rendre l'application .NET exécutable
RUN chmod +x "${HOMEDIR}/cs2app/WebApplication1.dll"

# Passer en tant qu’utilisateur root pour configurer entrypoint.sh
USER root

# Copier le script d'entrée et définir les permissions
COPY entrypoint.sh "${HOMEDIR}/entrypoint.sh"
RUN chmod +x "${HOMEDIR}/entrypoint.sh" && \
    dos2unix "${HOMEDIR}/entrypoint.sh"

# Repasser à l’utilisateur non-root pour exécuter SteamCMD et le serveur
USER "${USER}"

# Exposer le port du serveur (par défaut 27015)
EXPOSE 27015/udp
EXPOSE 27015/tcp

# Démarrer le serveur CS2 via le script d'entrée
CMD ["./entrypoint.sh"]
