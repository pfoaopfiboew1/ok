import numpy as np
import time

def process_data(data):
    rates = np.full(2000000, data.get("rate", 1.0), dtype=np.float64)
    mean_val = float(np.mean(rates))
    std_val = float(np.std(rates))
    return {
        "timestamp": time.time(),
        "pair": data.get("pair", "UNKNOWN"),
        "average_rate": mean_val,
        "std_dev": std_val,
        "source": data.get("kind", "UNKNOWN"),
        "cid": data.get("cid", "UNKNOWN")
    }