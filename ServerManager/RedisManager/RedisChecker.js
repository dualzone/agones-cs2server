import RedisKeyNotFountException from "../Exceptions/RedisKeyNotFountException.js";

export async function checkRedisValues(redis, serverUUID){


    await redis.exists(`server:${serverUUID}:team1:players`);
    //console.log(value)

    let error = false;

    if(! await redis.exists(`server:${serverUUID}:team1:players`, (err) => {})) error = true;
    if(!await redis.exists(`server:${serverUUID}:team2:players`)) error = true;
    if(!await redis.exists(`server:${serverUUID}:config`)) error = true;


    if (error) {
        await redis.publish(`server:${serverUUID}`, 'error-undefined-values')
        throw new RedisKeyNotFountException(`server:${serverUUID}`)
    }

}

