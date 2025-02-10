import os
from pathlib import Path
import subprocess
from platform import system
from threading import Thread

from utils.configureCS2Modding import ConfigureCS2Modding
from utils.definitions.serverConfig import Game
from utils.envManager import EnvManager
from utils.redis.redisClient import RedisClient
from manager.managerHelper import ManagerHelper
import uuid

class ServerManager:
    def __init__(self, steam_token, rcon_password, server_port=27015):
        self.__steam_token = steam_token
        self.__rcon_password = rcon_password
        self.__server_port = server_port
        self.__redis_client: RedisClient = RedisClient()
        self.__server_id = "3336752b-4d6e-4668-a39a-a963019a0c57" #str(uuid.uuid4())
        self.__helper: MangerHelper = ManagerHelper(self.__server_id)
        self.__allocator_thread: Thread = self.__redis_client.listen_for_events('gameserver:allocate', self.__redis_event_handler)
        self.__command_thread: Thread = self.__redis_client.listen_for_events('gameserver:command', self.__listen_to_commands)
        home_dir = EnvManager.get_env_var("HOMEDIR")
        bin_dir = 'linuxsteamrt64' if  system() == "Linux" else "win64"
        self.__launcher_path = Path(home_dir).expanduser() / "cs2server/game/bin" / bin_dir
        self.__configure_process()
        self.__helper.set_server_ready()
        self.__allocator_thread.start()
        self.__command_thread.start()

    def __configure_process(self):
        args = [
            '-dedicated',
            f'-port 27015',
            '-console',
            f'+sv_setsteamaccount  {self.__steam_token}',
            '-usercon',
            '+sv_lan 0',
            f'+rcon_password {self.__rcon_password}',
            '+game_type 2',
            '+game_mode 0',
            '+map de_dust2'
        ]

        print(self.__launcher_path)
        launcher_ext = '.exe' if system() != "Linux" else ""
        launch_path = self.__launcher_path / ('cs2' + launcher_ext)
        print(launch_path)
        self.__cs2_server_process = subprocess.Popen(
            [str(launch_path)] + args,
            cwd=str(self.__launcher_path),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        print("Configuration du modding sur CS2")
        configurator: ConfigureCS2Modding = ConfigureCS2Modding()
        configurator.ensure_modding_line()

        self.__listen_to_output()

    def __listen_to_output(self):
        def read_stream(stream, prefix):
            for line in iter(stream.readline, ''):
                if 'CTextConsoleWin::GetLine: !GetNumberOfConsoleInputEvents' in line: continue
                print(f'[{prefix}]: {line.strip()}')

        import threading
        threading.Thread(target=read_stream, args=(self.__cs2_server_process.stdout, 'CS2'), daemon=True).start()
        threading.Thread(target=read_stream, args=(self.__cs2_server_process.stderr, 'Erreur CS2'), daemon=True).start()

    def stop_server(self):
        if self.__cs2_server_process and self.__cs2_server_process.poll() is None:
            print('Arrêt du serveur CS2...')
            self.__cs2_server_process.terminate()
            self.__cs2_server_process.wait()
            print('Serveur CS2 arrêté.')
            self.__server_exit_handler()
        else:
            print('Le serveur CS2 n\'est pas en cours d\'exécution.')

    def send_command(self, command):
        if self.__cs2_server_process and self.__cs2_server_process.poll() is None:
            self.__cs2_server_process.stdin.write(command + '\n')
            self.__cs2_server_process.stdin.flush()
            print(f'Commande envoyée : {command}')
        else:
            print('Le serveur CS2 n\'est pas en cours d\'exécution.')

    def wait_for_server_exit(self):
        print('En attente de la fin du processus CS2...')
        self.__cs2_server_process.wait()
        print('Le processus CS2 s\'est terminé.')
        self.__server_exit_handler()

    def __server_exit_handler(self):
        self.__helper.set_server_shutdown()
        self.__redis_client.close()

    def __redis_event_handler(self, message):
        print(f"Received message: {message}")
        if message == self.__server_id:
            config: Game = self.__helper.set_server_allocated()
            self.send_command(f'get5_loadmatch_url http://localhost:8081/config/{self.__server_id}')

    def __listen_to_commands(self, message):
        print(f"Received message: {message}")
        self.send_command(message)
