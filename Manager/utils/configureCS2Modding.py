import os
from utils.envManager import EnvManager

class ConfigureCS2Modding:
    def __init__(self):
        self.file_path = "/home/steam/cs2server/game/csgo/gameinfo.gi"

    def ensure_modding_line(self):
        """ Vérifie et ajoute la ligne nécessaire pour Metamod si elle est absente. """
        modding_line = "                        Game    csgo/addons/metamod"
        target_line  = "                        Game    csgo"

        if not os.path.isfile(self.file_path):
            print(f"Erreur : le fichier {self.file_path} n'existe pas.")
            return

        with open(self.file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Vérifier si la ligne existe déjà
        if any(modding_line.strip() == line.strip() for line in lines):
            print("La ligne existe déjà, aucune modification nécessaire.")
            return

        # Insérer la ligne avant "Game    csgo"
        new_lines = []
        inserted = False
        for line in lines:
            if line.strip() == target_line.strip() and not inserted:
                new_lines.append(modding_line + "\n")
                inserted = True
            new_lines.append(line)

        # Écriture dans le fichier
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.writelines(new_lines)

        print("Ligne ajoutée avec succès.")


