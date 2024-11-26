import AgonesSDK from "@google-cloud/agones-sdk";// Assuming there is an Agones SDK for Node.js
import CS2Server from './CSServer.js';

async function main() {
    const agonesSdk = new AgonesSDK();

    // Ensure the Agones SDK is ready to handle the server
    await agonesSdk.connect();

    const steamToken = process.env.CS2_STEAM_TOKEN;
    if (!steamToken) throw new Error('La variable d\'environnement CS2_STEAM_TOKEN est introuvable.');

    const rconPassword = process.env.CS2_RCON_PASSWORD;
    if (!rconPassword) throw new Error('La variable d\'environnement CS2_RCON_PASSWORD est introuvable.');

    // Launch the CS2 server
    const server = new CS2Server(steamToken, rconPassword);

    server.startServer();
    await agonesSdk.ready();

    await server.waitForServerExit();
    await healthCheckLoop();

    // Inform Agones that the server is shutting down
    await agonesSdk.shutdown();
}

async function healthCheckLoop() {
    const agonesSdk = new AgonesSDK();
    while (true) {
        await agonesSdk.health();
        console.log('[HEALTH] send health ping');
        await new Promise(resolve => setTimeout(resolve, 10000)); // Send health ping every 10 seconds
    }
}

main().catch(err => console.error(err));
