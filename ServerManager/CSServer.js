import path from 'path';
import spawn from 'child_process';

export default class CS2Server {
    constructor(steamToken, rconPassword, gameType = 0, gameMode = 2, map = 'de_dust2', serverPort = 27015, launcherPath = '/cs2server/game/bin/linuxsteamrt64/') {
        this.steamToken = steamToken;
        this.rconPassword = rconPassword;
        this.gameType = gameType;
        this.gameMode = gameMode;
        this.map = map;
        this.serverPort = serverPort;

        const homeDir = process.env.HOMEDIR;
        if (!homeDir) throw new Error('La variable d\'environnement HOMEDIR est introuvable.');
        this.launcherPath = path.join(homeDir, launcherPath);

        this.configureProcess();
    }

    configureProcess() {
        const args = [
            '-dedicated',
            '-port', `${this.serverPort}`,
            '-console',
            '-usercon',
            `+sv_setsteamaccount ${this.steamToken}`,
            `+game_type ${this.gameType}`,
            `+game_mode ${this.gameMode}`,
            `+map ${this.map}`,
            '+sv_lan 0',
            `+rcon_password '${this.rconPassword}'`
        ];

        this.cs2ServerProcess = spawn(path.join(this.launcherPath, 'cs2'), args, {
            cwd: this.launcherPath,
            stdio: ['pipe', 'pipe', 'pipe']  // Use pipes for stdin, stdout, stderr
        });

        this.cs2ServerProcess.stdout.on('data', (data) => {
            console.log(`[CS2]: ${data.toString()}`);
        });

        this.cs2ServerProcess.stderr.on('data', (data) => {
            console.error(`[Erreur CS2]: ${data.toString()}`);
        });

        this.cs2ServerProcess.on('exit', () => {
            console.log('Le processus CS2 s\'est terminé.');
        });
    }

    startServer() {
        console.log('Démarrage du serveur CS2...');
        this.cs2ServerProcess.start();
        console.log('Le serveur CS2 est en cours d\'exécution...');
    }

    stopServer() {
        if (!this.cs2ServerProcess.killed) {
            console.log('Arrêt du serveur CS2...');
            this.cs2ServerProcess.kill();
            console.log('Serveur CS2 arrêté.');
        } else {
            console.log('Le serveur CS2 n\'est pas en cours d\'exécution.');
        }
    }

    sendCommand(command) {
        if (!this.cs2ServerProcess.killed) {
            this.cs2ServerProcess.stdin.write(command + '\n');
            console.log(`Commande envoyée : ${command}`);
        } else {
            console.log('Le processus CS2 n\'est pas en cours d\'exécution.');
        }
    }

    waitForServerExit() {
        console.log('En attente de la fin du processus CS2...');
        this.cs2ServerProcess.on('exit', () => {
            console.log('Le processus CS2 s\'est terminé.');
        });
    }
}
