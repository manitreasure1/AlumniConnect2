import redis

jwt_redis_block_list = redis.StrictRedis(
    host='localhost', port=6379, db=0, decode_responses=True
)