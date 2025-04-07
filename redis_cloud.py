import redis

# Initialize Redis connection
redis_cloud = redis.Redis(
    host='redis-cloud.com',
    port=12345,
    decode_responses=True,
    username="default",
    password="password",
)
