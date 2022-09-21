import redis

from echo_service.core.config import config

redis = redis.from_url(url=f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}", decode_responses=True)
