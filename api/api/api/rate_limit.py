import redis
from datetime import datetime, timedelta

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Constants for rate limiting
REQUEST_LIMIT = 100  # Number of requests allowed per time window
TIME_WINDOW = 60  # Time window in seconds

def get_key(api_key, endpoint):
    # Generate a unique key for rate limiting based on API key and endpoint
    return f"{api_key}:{endpoint}"

def rate_limit_exceeded(api_key, endpoint):
    # This function checks if the request limit has been exceeded for the given API key and endpoint
    key = get_key(api_key, endpoint)
    count = redis_client.get(key)
    return int(count) >= REQUEST_LIMIT if count else False

def update_request_count(api_key, endpoint):
    # This function updates the request count for the given API key and endpoint
    key = get_key(api_key, endpoint)
    count = redis_client.incr(key)
    if count == 1:
        # Set the expiration time based on ISO 8601 formatted timestamp
        expire_at = (datetime.utcnow() + timedelta(seconds=TIME_WINDOW)).isoformat()
        redis_client.setex(key, TIME_WINDOW, expire_at)
