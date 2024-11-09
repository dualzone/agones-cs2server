# Étape 1 : Compiler le projet C# (build stage)
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /app

# Copier le code source C# dans le conteneur
COPY WebApplication1/ ./src/

# Compiler l'application C#
RUN dotnet publish ./src -c Release -o /out

# Étape 2 : Créer l'image de base et configurer l'environnement
FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS base

# Installer les dépendances et configurer les locales
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    locales \
    locales-all \
    lib32gcc-s1 \
    net-tools \
    curl \
    unzip \
    lib32stdc++6 \
    libc6-dev \
    wget \
    libc6-i386 \
    libtcmalloc-minimal4 \
    dos2unix && \
    localedef -i en_US -f UTF-8 en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

# Définir les variables d'environnement pour les locales
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

# Installer .NET Runtime 8.0.0 nécessaire pour l'application
RUN wget https://dotnet.microsoft.com/download/dotnet/scripts/v1/dotnet-install.sh && \
    chmod +x dotnet-install.sh && \
    ./dotnet-install.sh --channel 8.0 --runtime aspnetcore --install-dir /usr/share/dotnet && \
    rm dotnet-install.sh

# Ajouter /usr/share/dotnet à la variable PATH
ENV PATH="${PATH}:/usr/share/dotnet"

# Télécharger et installer SteamCMD dans /home/cs2user/Steam
RUN mkdir -p /home/cs2user/Steam && \
    curl -sSL http://media.steampowered.com/installer/steamcmd_linux.tar.gz | tar -xz -C /home/cs2user/Steam

# Installer le runtime Steam
RUN mkdir -p /home/cs2user/.steam/sdk32 && \
    ln -s /home/cs2user/Steam/linux32/steamclient.so /home/cs2user/.steam/sdk32/steamclient.so

# Créer un utilisateur non-root pour exécuter le serveur
RUN useradd -m cs2user && \
    mkdir -p /root/Steam && \
    mkdir -p /home/cs2user/Steam && \
    mkdir -p /home/cs2user/cs2_server && \
    chown -R cs2user:cs2user /root/Steam /home/cs2user/Steam /home/cs2user/cs2_server && \
    chmod -R 740 /home/cs2user/Steam && \
    chmod -R 770 /home/cs2user/cs2_server && \
    chmod -R 770 /root/Steam

# Définir le répertoire de travail pour SteamCMD et le serveur
WORKDIR /home/cs2user

# Copier l'exécutable C# depuis l'étape de compilation
COPY --from=build /out /home/cs2user/cs2_app

# Rendre l'application .NET exécutable
RUN chmod +x /home/cs2user/cs2_app/WebApplication1.dll

# Copier et configurer SteamCMD
RUN curl -sSL http://media.steampowered.com/installer/steamcmd_linux.tar.gz | tar -xz && \
    chmod +x /home/cs2user/Steam/steamcmd.sh && \
    chmod -R +x /home/cs2user/Steam/linux32/steamcmd

# Passer en tant qu’utilisateur root pour configurer entrypoint.sh
USER root

# Copier le script d'entrée et définir les permissions
COPY entrypoint.sh /home/cs2user/entrypoint.sh
RUN chmod +x /home/cs2user/entrypoint.sh && \
    dos2unix /home/cs2user/entrypoint.sh

# Repasser à l’utilisateur non-root pour exécuter SteamCMD et le serveur
USER cs2user

# Exposer le port du serveur (par défaut 27015)
EXPOSE 27015/udp
EXPOSE 27015/tcp

# Démarrer le serveur CS2 via le script d'entrée
CMD ["/home/cs2user/entrypoint.sh"]
