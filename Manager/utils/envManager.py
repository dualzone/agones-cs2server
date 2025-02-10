import os

class EnvManager:
    @staticmethod
    def get_env_var(var_name, default=None):
        """Récupère une variable d'environnement, soit depuis os, soit depuis .env."""
        return os.getenv(var_name, default)