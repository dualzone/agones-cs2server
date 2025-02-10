import json
import os

from utils.envManager import EnvManager


class ConfigureLan:
    def __init__(self):
        self.file_path = EnvManager.get_env_var("HOMEDIR") + "/cs2server/game/csgo/PugSharp/Config/server.json"
        self.default_config = {
            "locale": "fr",
            "allow_players_without_match": False
        }

    def write_config(self):
        """Écrit ou met à jour le fichier JSON avec la configuration par défaut."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as file:
                    existing_data = json.load(file)

                # Vérifier si la configuration est déjà correcte
                if existing_data == self.default_config:
                    print("✅ La configuration est déjà à jour.")
                    return

            except json.JSONDecodeError:
                print("⚠️ Fichier corrompu ou non valide. Il sera réécrit.")

        # Écriture du fichier JSON
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.default_config, file, indent=4)
            print(f"✅ Configuration mise à jour dans {self.file_path}")


