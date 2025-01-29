import AgonesSDK from "@google-cloud/agones-sdk";// Assuming there is an Agones SDK for Node.js
import CS2Server from './CSServer.js';
import ConsoleLogger from "./Logger/ConsoleLogger.js";
import EnvNotFoudException from "./Exceptions/EnvNotFoudException.js";
import fs from 'fs';
import dotenv from 'dotenv';

async function main() {
    const agonesSdk = new AgonesSDK();

    // Load from .env if exists
    if (fs.existsSync('.env')) {
        dotenv.config();
        ConsoleLogger.info('SYSTEM', 'Loaded .env file');
    }

    checkEnv();

    const steamToken = process.env.CS2_STEAM_TOKEN;

    const rconPassword = process.env.CS2_RCON_PASSWORD;

    ConsoleLogger.info('SYSTEM', 'Try to connect to Agones');

    await agonesSdk.connect();

    ConsoleLogger.info('SYSTEM', 'Connected to Agones');

    // Launch the CS2 server
    const server = new CS2Server(steamToken, rconPassword, agonesSdk);

    healthCheckLoop();

    const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
    await delay(35000);

    await server.waitForServerExit();

    // Inform Agones that the server is shutting down
    await agonesSdk.shutdown();
}

async function healthCheckLoop() {
    const agonesSdk = new AgonesSDK();
    while (true) {
        await agonesSdk.health();
        ConsoleLogger.info('HEALTH', 'Health check sent');
        await new Promise(resolve => setTimeout(resolve, 10000)); // Send health ping every 10 seconds
    }
}

function checkEnv() {
    const envs = [
        'CS2_STEAM_TOKEN',
        'CS2_RCON_PASSWORD',
        'REDIS_PASSWORD',
        'REDIS_HOST',
        'REDIS_PORT',
        'HOME_DIR'
    ];

    for (const env of envs) {
        if (!process.env[env]) {
            throw new EnvNotFoudException(env);
        }
    }
}

main().catch(err => ConsoleLogger.error('SYSTEM', err.message));
