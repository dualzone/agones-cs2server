import ConsoleLogger from "../Logger/ConsoleLogger.js";

export default class EnvNotFoudException extends Error {
  constructor(envName) {
    super(`Environment variable ${envName} not found`);
    this.name = 'EnvNotFoudException';
    ConsoleLogger.error('SYSTEM', `Environment variable ${envName} not found`);
  }
}