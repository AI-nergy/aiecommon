import time
import logging

def log_time(message):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            logging.info(f"{message}: {func.__name__} took {round(elapsed_time,2)} seconds")
            return result
        return wrapper
    return decorator