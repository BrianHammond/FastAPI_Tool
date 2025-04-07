import redis

# Initialize Redis connection
redis_cloud = redis.Redis(
    host='redis-14416.c290.ap-northeast-1-2.ec2.redns.redis-cloud.com',
    port=14416,
    decode_responses=True,
    username="default",
    password="iRPQGAP1U7pxPRRiFoysfX4POkR0B5R4",
)