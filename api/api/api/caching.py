# caching.py
from functools import wraps

def cache_response(timeout=300):
    # Function decorator to cache responses for read-only endpoints
    def decorator(func):
        cache = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            if key in cache and time.time() - cache[key]['timestamp'] < timeout:
                return cache[key]['response']
            else:
                response = func(*args, **kwargs)
                cache[key] = {'response': response, 'timestamp': time.time()}
                return response

        return wrapper

    return decorator
