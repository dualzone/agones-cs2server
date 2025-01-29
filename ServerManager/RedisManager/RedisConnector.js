import {createClient} from "redis";
import ConsoleLogger, {tags} from "../Logger/ConsoleLogger.js";

export default class RedisConnector {

    #client = null;

    async connect(database = 10) {
        this.#client = createClient({
            socket: {
                host: process.env.REDIS_HOST,
                port: process.env.REDIS_PORT
            },
            password: process.env.REDIS_PASSWORD,
            database: database
        });

        this.#client.on('error', err => {
            ConsoleLogger.error(tags.SYSTEM, "Error " + err)
            process.exit(1)
        });
        this.#client.on('ready', () => ConsoleLogger.info(tags.SYSTEM, 'Redis is ready'));
        this.#client.on('connect', () => ConsoleLogger.info(tags.SYSTEM, 'Connected to Redis'));
        this.#client.on('reconnecting', () => ConsoleLogger.warn(tags.SYSTEM, 'Reconnecting to Redis'));
        await this.#client.connect()

    }

    async disconnect() {
        await this.#client.unsubscribe();
        this.#client.disconnect();
    }

    async subscribe(channel, listener) {
        const subscriber = this.#client.duplicate()
        await subscriber.connect()
        ConsoleLogger.info(tags.SYSTEM, `Subscribed to ${channel} with new client`);
        await subscriber.subscribe(channel, listener);
        return subscriber;
    }

    async unsubscribe(channel, subscriber) {
        await subscriber.unsubscribe(channel);
        await subscriber.disconnect();
    }


    get client() {
        return this.#client;
    }
}

