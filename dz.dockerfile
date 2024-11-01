# Étape 1 : Compiler le projet C# (build stage)
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /app

# Copier le code source C# dans le conteneur
COPY src/ ./src/

# Compiler l'application C#
RUN dotnet publish ./src -c Release -o /out

# Étape 2 : Créer l'image finale avec SteamCMD et le serveur CS2
FROM debian:bullseye-slim

# Installer les dépendances requises pour SteamCMD et CS2
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        lib32gcc-s1 \
        curl \
        unzip \
        lib32stdc++6 \
        libtcmalloc-minimal4 && \
    rm -rf /var/lib/apt/lists/*

# Créer un utilisateur non-root pour exécuter le serveur
RUN useradd -m cs2user

# Définir le répertoire de travail pour SteamCMD et le serveur
WORKDIR /home/cs2user

# Copier l'exécutable C# depuis l'étape de compilation
COPY --from=build /out /home/cs2user/cs2_app

# Rendre l'application .NET exécutable
RUN chmod +x /home/cs2user/cs2_app/WebApplication

# Télécharger et installer SteamCMD
RUN curl -sSL http://media.steampowered.com/installer/steamcmd_linux.tar.gz | tar -xz

# Créer un répertoire pour le serveur CS2
RUN mkdir -p /home/cs2user/cs2_server

# Passer en tant qu'utilisateur non-root
USER cs2user

# Créer le script d'entrée
COPY entrypoint.sh /home/cs2user/entrypoint.sh
RUN chmod +x /home/cs2user/entrypoint.sh

# Exposer le port du serveur (par défaut 27015)
EXPOSE 27015/udp

# Démarrer l'exécutable C# pour lancer le serveur CS2
ENTRYPOINT ["/home/cs2user/entrypoint.sh"]
