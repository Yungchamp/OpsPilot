import time

def backoff(attempts: int) -> int:
    # exponential backoff seconds
    return min(60, (2 ** attempts))
