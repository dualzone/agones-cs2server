from pathlib import Path
import subprocess
from ..utils.envManager import EnvManager

class ServerManager:
    def __init__(self, steam_token, rcon_password, launcher_path='/cs2server/game/bin/linuxsteamrt64/', server_port=27015):
        self.__steam_token = steam_token
        self.__rcon_password = rcon_password
        self.__server_port = server_port

        home_dir = EnvManager.get_env_var("TEST")
        self.__launcher_path = home_dir / launcher_path

        if not self.__launcher_path.exists():
            raise FileNotFoundError(f"Le chemin du lanceur CS2 est introuvable : {self.__launcher_path}")

        self.__configure_process()

    def __configure_process(self):
        args = [
            '-dedicated',
            '-port', str(self.__server_port),
            '-console',
            '-usercon',
            '+sv_lan 1',
            f'+rcon_password {self.__rcon_password}'
        ]

        self.__cs2_server_process = subprocess.Popen(
            [str(self.__launcher_path / 'cs2')] + args,
            cwd=str(self.__launcher_path),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        self.__listen_to_output()

    def __listen_to_output(self):
        def read_stream(stream, prefix):
            for line in iter(stream.readline, ''):
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
