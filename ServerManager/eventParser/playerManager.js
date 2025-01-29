export default class  PlayerManager {
    constructor(redisConnector, server,) {
        this.redisConnector = redisConnector;
        this.agonesSdk = agonesSdk;
        this.uuid = uuid;
    }

    kickPlayer(uuid){
        //Kick player from the server
    }

    banPlayer(uuid){
        //Ban player from the server
    }
}