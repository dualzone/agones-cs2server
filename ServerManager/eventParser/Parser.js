import ConsoleLogger, {tags} from "../Logger/ConsoleLogger.js";

export default class Parser {

    constructor(redisConnector, server, agonesSdk, uuid) {
        this.redisConnector = redisConnector;
        this.server = server;
        this.agonesSdk = agonesSdk;
        this.uuid = uuid;
    }

    parseEvent(gameEvent){
        switch (true){
            case gameEvent.includes('CSource2Server::GameServerSteamAPIActivated()'):
                this.redisConnector.client.publish(`server:${this.uuid}`, 'ServerReady')
                this.agonesSdk.ready();
                break;




            default: break;
        }

    }



}


