const redis = require('redis');

const { REDIS_PORT, REDIS_HOST } = process.env;
const client = redis.createClient(REDIS_PORT, REDIS_HOST);

client.on('connect', function () {
    console.log('Connected to Redis!');
});
