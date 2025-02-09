import os
from utils.envManager import EnvManager
from serverManager import serverManager



def main():
    EnvManager.get_env_var("TEST")
    print("Hello, World!")
    print("Launching server...")
    server = serverManager(EnvManager.get_env_var("CS2_STEAM_TOKEN"), EnvManager.get_env_var("CS2_RCON_PASSWORD"), "")


if __name__ == "__main__":
    main()
