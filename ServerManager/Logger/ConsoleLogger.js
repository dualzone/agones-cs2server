
const colors = {
    BACK: "\x1b[30m",
    RED: "\x1b[31m",
    GREEN: "\x1b[32m",
    YELLOW: "\x1b[33m",
    BLUE: "\x1b[34m",
    MAGENTA: "\x1b[35m",
    CYAN: "\x1b[36m",
    WHITE: "\x1b[37m",
    GRAY: "\x1b[90m",
}

const background = {
    BACK: "\x1b[40m",
    RED: "\x1b[41m",
    GREEN: "\x1b[42m",
    YELLOW: "\x1b[43m",
    BLUE: "\x1b[44m",
    MAGENTA: "\x1b[45m",
    CYAN: "\x1b[46m",
    WHITE: "\x1b[47m",
    GRAY: "\x1b[100m",
}

const format = {
    RESET: "\x1b[0m",
    BRIGHT: "\x1b[1m",
    DIM: "\x1b[2m",
    UNDERSCORE: "\x1b[4m",
    BLINK: "\x1b[5m",
    REVERSE: "\x1b[7m",
    HIDDEN: "\x1b[8m",
}

export const tags = {
    CS2: "[CS2]",
    SYSTEM: "[SYSTEM]",
    HEALTH: "[HEALTH]",
    EVENTS: "[EVENT]",
}

const levels = {
    INFO: "(INFO)",
    WARN: "(WARN)",
    ERROR: "(ERROR)",
}

export default class ConsoleLogger {

    static test(){
        console.log("test")
    }

    static getTime() {
        const date = new Date();
        return `${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
    }

    static warn(tag, message) {
        console.log(`${colors.YELLOW} ${this.getTime()} ${tags[tag]} ${levels.WARN} : ${message}${format.RESET}`);
    }

    static info(tag, message) {
        if (tag.startsWith("[")){
            tag = tag.replace("[", "").replace("]", "");
        }

        switch (tag){
            case "CS2":
                console.log(`${colors.MAGENTA}${this.getTime()} ${tags[tag]} ${levels.INFO} : ${message}${format.RESET}`);
                break;
            case "SYSTEM":
                console.log(`${colors.GREEN}${this.getTime()} ${tags[tag]} ${levels.INFO} : ${message}${format.RESET}`);
                break;
            case "HEALTH":
                console.log(`${colors.CYAN}${this.getTime()} ${tags[tag]} ${levels.INFO} : ${message}${format.RESET}`);
                break;
            case "EVENTS":
                console.log(`${colors.BLUE}${this.getTime()} ${tags[tag]} ${levels.INFO} : ${message}${format.RESET}`);
                break;
        }
    }

    static error(tag, message) {
        console.log(`${colors.RED} ${this.getTime()} ${tags[tag]} ${levels.ERROR} : ${message}${format.RESET}`);
    }


}