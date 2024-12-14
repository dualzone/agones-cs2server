import path from 'path';
import { spawn } from 'child_process';
import {createClient} from "redis";
import ConsoleLogger, {tags} from "./Logger/ConsoleLogger.js";

export default class CS2Server {
    constructor(steamToken, rconPassword, gameType = 0, gameMode = 2, map = 'de_dust2', serverPort = 27015, launcherPath = '/cs2-server/game/bin/win64/') {
        this.steamToken = steamToken;
        this.rconPassword = rconPassword;
        this.gameType = gameType;
        this.gameMode = gameMode;
        this.map = map;
        this.serverPort = serverPort;

        const homeDir = process.env.HOME_DIR;
        this.launcherPath = path.join(homeDir, launcherPath);

        this.redis = null

        this.createRedisClient().catch((err) => console.error(err))
        this.configureProcess();
    }

    async createRedisClient() {
        this.redis = await createClient()
            .on('error', (err) => ConsoleLogger.error(tags.SYSTEM, err))
            .on('connect', () => ConsoleLogger.info(tags.SYSTEM, 'Connecté à Redis'))
            .connect()
    }

    async disconnectRedis() {
        if(this.redis) {
            await this.redis.disconnect()
            ConsoleLogger.info(tags.SYSTEM, 'Déconnecté de Redis')
        }else {
            ConsoleLogger.warn(tags.SYSTEM, 'Redis n\'est pas connecté')
        }
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

        this.cs2ServerProcess = spawn(path.join(this.launcherPath, 'cs2.exe'), args, {
            cwd: this.launcherPath,
            stdio: ['pipe', 'pipe', 'pipe']  // Use pipes for stdin, stdout, stderr
        });

        this.cs2ServerProcess.stdout.on('data', (data) => {
            if (data.toString().includes('CTextConsoleWin::GetLine')) return;
            ConsoleLogger.info('CS2', data.toString());
        });

        this.cs2ServerProcess.stderr.on('data', (data) => {
            ConsoleLogger.error('CS2', data.toString());
        });

        this.cs2ServerProcess.on('exit', () => {
            this.disconnectRedis().catch((err) => console.error(err))
            ConsoleLogger.info(tags.SYSTEM, 'Le processus CS2 s\'est terminé.');
        });

    }


    sendCommand(command) {
        if (!this.cs2ServerProcess.killed) {
            this.cs2ServerProcess.stdin.write(command + '\n');
            ConsoleLogger.info(tags.SYSTEM, `Commande envoyée au serveur CS2 : ${command}`);
        } else {
            ConsoleLogger.warn(tags.SYSTEM, 'Le processus CS2 n\'est pas en cours d\'exécution.');
        }
    }

    waitForServerExit() {
        ConsoleLogger.info(tags.SYSTEM, 'En attente de la fin du processus CS2...');
        this.cs2ServerProcess.on('exit', () => {
            ConsoleLogger.info(tags.SYSTEM, 'Le processus CS2 s\'est terminé.');
        });
    }
}
