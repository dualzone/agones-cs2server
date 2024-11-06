# Étape 1 : Compiler le projet C# (build stage)
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /app

# Copier le code source C# dans le conteneur
COPY WebApplication1/ ./src/

# Compiler l'application C#
RUN dotnet publish ./src -c Release -o /out

FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS base

# Installer les dépendances et configurer les locales
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    lib32gcc-s1 \
    net-tools \
    curl \
    unzip \
    lib32stdc++6 \
    libc6-dev \
    wget \
    libtcmalloc-minimal4 \
    dos2unix \
    locales && \
    rm -rf /var/lib/apt/lists/*

# Générer la locale en_US.UTF-8 sans utiliser `update-locale`
RUN locale-gen en_US.UTF-8

# Définir les variables d'environnement pour les locales
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

# Installer les packages .NET après la configuration des locales
RUN wget https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb -O packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    dotnet-sdk-8.0 \
    aspnetcore-runtime-8.0 \
    dotnet-runtime-8.0 && \
    rm packages-microsoft-prod.deb && \
    rm -rf /var/lib/apt/lists/*

# Créer un utilisateur non-root pour exécuter le serveur
RUN useradd -m cs2user && \
    mkdir -p /root/Steam && \
    chown -R cs2user:cs2user /root/Steam && \
    chmod -R 755 /root/Steam

# Définir le répertoire de travail pour SteamCMD et le serveur
WORKDIR /home/cs2user

# Copier l'exécutable C# depuis l'étape de compilation
COPY --from=build /out /home/cs2user/cs2_app

# Rendre l'application .NET exécutable
RUN chmod +x /home/cs2user/cs2_app/WebApplication1

# Télécharger et installer SteamCMD
RUN curl -sSL http://media.steampowered.com/installer/steamcmd_linux.tar.gz | tar -xz

# Créer un répertoire pour le serveur CS2
RUN mkdir -p /home/cs2user/cs2_server

# Passer en tant qu'utilisateur non-root

# Créer le script d'entrée
COPY entrypoint.sh /home/cs2user/entrypoint.sh
RUN chown -R cs2user:cs2user /home/cs2user
RUN chmod +x /home/cs2user/entrypoint.sh
RUN dos2unix /home/cs2user/entrypoint.sh

# Exposer le port du serveur (par défaut 27015)
EXPOSE 27015/udp
EXPOSE 27015/tcp

# Démarrer l'exécutable C# pour lancer le serveur CS2
CMD ["/home/cs2user/entrypoint.sh"]