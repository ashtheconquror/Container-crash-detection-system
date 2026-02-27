# Helper functions

from collections import deque

def rolling_buffer(max_len):
    return deque(maxlen=max_len)
