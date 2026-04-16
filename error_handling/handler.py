import time
import random

def retry(func, attempts=3, delay=1, backoff=2):
    """Retry a function with exponential backoff."""
    for i in range(attempts):
        try:
            return func()
        except Exception as e:
            print(f"Attempt {i+1} failed: {e}")
            if i == attempts - 1:
                raise
            sleep_time = delay * (backoff ** i) + random.uniform(0, 1)
            time.sleep(sleep_time)

def circuit_breaker(func, failure_threshold=3, recovery_timeout=30):
    """Implement a circuit breaker pattern."""
    state = "CLOSED"
    failure_count = 0
    last_failure_time = None

    def wrapper(*args, **kwargs):
        nonlocal state, failure_count, last_failure_time

        if state == "OPEN":
            if time.time() - last_failure_time > recovery_timeout:
                state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            failure_count = 0
            state = "CLOSED"
            return result
        except Exception as e:
            failure_count += 1
            last_failure_time = time.time()

            if failure_count >= failure_threshold:
                state = "OPEN"
                raise Exception("Circuit breaker is OPEN") from e
            raise
    return wrapper