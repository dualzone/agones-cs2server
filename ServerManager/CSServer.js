import path from 'path';
import { spawn } from 'child_process';
import {createClient} from "redis";
import ConsoleLogger, {tags} from "./Logger/ConsoleLogger.js";
import Parser from "./eventParser/Parser.js";
import {checkRedisValues} from "./RedisManager/RedisChecker.js";
import RedisConnector from "./RedisManager/RedisConnector.js";

const isWin = process.platform === "win32";

export default class CS2Server {
    constructor(steamToken, rconPassword, agonesSdk, gameType = 0, gameMode = 2, map = 'de_dust2', serverPort = 27015, launcherPath = '/cs2server/game/bin/' + (isWin ? 'win64' : 'linuxsteamrt64')) {
        this.steamToken = steamToken;
        this.rconPassword = rconPassword;
        this.gameType = gameType;
        this.gameMode = gameMode;
        this.map = map;
        this.serverPort = serverPort;
        this.agonesSdk = agonesSdk;
        this.uuid = "";
        this.waitingToRegister = true;




        const homeDir = process.env.HOME_DIR;
        this.launcherPath = path.join(homeDir, launcherPath);

        this.redis = new RedisConnector();
        this.#starter()
    }

    // This function is used  to prepare redis Client check values
    async #starter() {

        await this.redis.connect()

        await this.#registerServer()

        ConsoleLogger.info(tags.SYSTEM, 'Next')

        this.redisEventClient =  await this.redis.subscribe(`server:${this.uuid}`, this.#redisChannelListener)

        await this.#loadRedisValues()

        this.parser = new Parser(this.redis, this, this.agonesSdk, this.uuid);

        this.#configureProcess();
    }

    async #registerServer() {
        let start = Date.now()
        ConsoleLogger.info(tags.SYSTEM, 'Registering server')
        let redisRegister = await this.redis.subscribe('server:register', this.#registerCallBack)
        this.redis.client.publish(`server:register`, JSON.stringify({
            "event": "RegisterServer"
        }))
        while(this.waitingToRegister && Date.now() - start < 30000) {
            await new Promise(resolve => setTimeout(resolve, 1000))
        }
        if(this.waitingToRegister) {
            ConsoleLogger.error(tags.SYSTEM, 'Server failed to register')
            process.exit(1)
        }
        ConsoleLogger.info(tags.SYSTEM, 'Server registered')
        await redisRegister.disconnect()
    }

    #registerCallBack = (message, channel) => {
        let messageDecoded = JSON.parse(message)
        if('ServerRegistered' === messageDecoded.event) {
            ConsoleLogger.info(tags.SYSTEM, 'Server registered with uuid: ' + messageDecoded.uuid);
            this.uuid = messageDecoded.uuid
            this.waitingToRegister = false
        }
    }

    #redisChannelListener = (message, channel) => {
        switch (message) {
            case 'ServerRequested':
                ConsoleLogger.info(tags.SYSTEM, 'Server requested');
                this.agonesSdk.allocate();
                this.#loadRedisValues()
                this.sendCommand('unpause')
                this.sendCommand(`map ${this.map}`)
                this.sendCommand(`game_mode ${this.gameMode}`)
                this.sendCommand(`game_type ${this.gameType}`)
                this.sendCommand('sv_banid_enabled 1')
                this.sendCommand('sv_cheats 0')
                this.sendCommand('sv_lan 0')
                this.sendCommand('sv_voiceenable 1')
                this.sendCommand('sv_pausable 1')
                this.sendCommand('sv_pure 1')
                this.sendCommand('sv_pure_kick_clients 1')
                this.sendCommand('sv_pure_trace 1')
                this.sendCommand('restart')
                break
            case 'NewConfig':
                ConsoleLogger.info(tags.SYSTEM, 'New config received');
                this.redis.client.publish(`server:${this.uuid}`, 'ServerNotReady')
                this.#reconfigure();
                break;
            case 'ServerReady':
                ConsoleLogger.info(tags.SYSTEM, 'Server is ready but not requested pause the game');
                this.sendCommand('pause')
                break;

            default:
                break;
        }
    }

    async #loadRedisValues() {
        await checkRedisValues(this.redis.client, this.uuid)

        let config = await this.redis.client.hGetAll(`server:${this.uuid}:config`)

        this.gameType = config.type
        this.gameMode = config.mode
        this.map = config.map

    }


    #configureProcess() {
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

        this.cs2ServerProcess = spawn(path.join(this.launcherPath, 'cs2'+ (isWin ? '.exe' : '') ), args, {
            cwd: this.launcherPath,
            stdio: ['pipe', 'pipe', 'pipe']  // Use pipes for stdin, stdout, stderr
        });

        this.cs2ServerProcess.stdout.on('data', (data) => {
            if (isWin && data.toString().includes('CTextConsoleWin::GetLine')) return;
            this.parser.parseEvent(data.toString());
            ConsoleLogger.info('CS2', data.toString());
        });

        this.cs2ServerProcess.stderr.on('data', (data) => {
            ConsoleLogger.error('CS2', data.toString());
        });

        this.cs2ServerProcess.on('exit', () => {
            //this.redis.disconnect()
            ConsoleLogger.info(tags.SYSTEM, 'Le processus CS2 s\'est terminé.');
            //process.exit(0);
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
        if (!this.cs2ServerProcess) {
            ConsoleLogger.error(tags.SYSTEM, 'Le processus CS2 n\'est pas en cours d\'exécution.');
            process.exit(1);
        }
        ConsoleLogger.info(tags.SYSTEM, 'En attente de la fin du processus CS2...');
        this.cs2ServerProcess.on('exit', () => {
            ConsoleLogger.info(tags.SYSTEM, 'Le processus CS2 s\'est terminé.');
            this.redis.disconnect()
            process.exit(0);
        });
    }

    #reconfigure(){
        this.cs2ServerProcess.kill('SIGTERM');
        this.#configureProcess();
    }


}
