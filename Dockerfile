# Étape 1 : Compiler le projet C# (build stage)
FROM mcr.microsoft.com/dotnet/sdk:8.0-bookworm-slim AS build
WORKDIR /app
VOLUME /home/cs2user/cs2_server

# Copier le code source C# dans le conteneur
COPY WebApplication1/ ./src/

# Compiler l'application C#
RUN dotnet publish ./src -c Release -o /out

# Étape 2 : Créer l'image de base et configurer l'environnement
FROM mcr.microsoft.com/dotnet/aspnet:8.0-bookworm-slim AS base

# Installer les dépendances et configurer les locales
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    locales \
    locales-all \
    lib32gcc-s1 \
    curl \
    unzip \
    wget \
    net-tools &&\
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Définir les variables d'environnement pour les locales

# Ajouter SteamCMD
RUN mkdir -p /home/cs2user/Steam && \
    curl -sSL http://media.steampowered.com/installer/steamcmd_linux.tar.gz | tar -xz -C /home/cs2user/Steam && \
    chmod +x /home/cs2user/Steam/steamcmd.sh && \
    mkdir -p /home/cs2user/.steam/sdk64 && \
    ln -s /home/cs2user/Steam/linux64/steamclient.so /home/cs2user/.steam/sdk64/steamclient.so


# Télécharger et installer le runtime Steam nécessaire (sniper runtime) en vérifiant l'URL
RUN mkdir -p /home/cs2user/Steam/steamapps/common/SteamLinuxRuntime_sniper && \
    cd /home/cs2user/Steam/steamapps/common/SteamLinuxRuntime_sniper && \
    curl -O https://repo.steampowered.com/SteamLinuxRuntime_sniper.tar.xz && \
    file SteamLinuxRuntime_sniper.tar.xz && \
    tar -xJf SteamLinuxRuntime_sniper.tar.xz || echo "Extraction échouée. Vérifiez le fichier."

# Créer un utilisateur non-root pour exécuter le serveur
RUN useradd -m cs2user && \
    mkdir -p /root/Steam && \
    mkdir -p /home/cs2user/Steam && \
    mkdir -p /home/cs2user/cs2_server

# Définir le répertoire de travail pour SteamCMD et le serveur
WORKDIR /home/cs2user

USER root
# Copier l'exécutable C# depuis l'étape de compilation
COPY --from=build /out /home/cs2user/cs2_app
COPY entrypoint.sh /home/cs2user/entrypoint.sh

RUN chown -R cs2user:cs2user /root/Steam /home/cs2user /home/cs2user/.steam /home/cs2user/cs2_app  && \
    chmod -R 740 /home/cs2user && \
    chmod +x /home/cs2user/cs2_app/WebApplication1.dll && \
    chmod +x /home/cs2user/entrypoint.sh && \
    chown cs2user:cs2user /home/cs2user/entrypoint.sh

# Repasser à l’utilisateur non-root pour exécuter SteamCMD et le serveur
USER cs2user

# Exposer le port du serveur (par défaut 27015)
EXPOSE 27015/udp
EXPOSE 27015/tcp


# Démarrer le serveur CS2 via le script d'entrée
CMD ["/home/cs2user/entrypoint.sh"]
