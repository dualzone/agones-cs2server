import ConsoleLogger from "../Logger/ConsoleLogger.js";

export default class RedisKeyNotFountException extends Error {
    constructor(key) {
        super(`Redis key ${key} not found`);
        this.name = 'RedisKeyNotFountException';
        ConsoleLogger.error('SYSTEM', `Redis key ${key} not found`);
    }
}