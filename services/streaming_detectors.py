import numpy as np
from services.detector import predict


def detect_from_buffer(buffer):
    if len(buffer) < buffer.maxlen:
        return None, None
    signal = np.array(buffer)
    return predict(signal)
