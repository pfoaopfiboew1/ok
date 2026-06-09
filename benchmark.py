import time
import requests
import numpy as np
import random
from sources import ALL_REQUESTS

def run_sequential_baseline():
    start = time.time()
    for req in ALL_REQUESTS:
        if req["kind"] == "mock":
            time.sleep(random.uniform(0.1, 0.5))
            rate = random.uniform(0.5, 150.0)
        else:
            try:
                resp = requests.get(req["url"], timeout=5)
                if resp.status_code == 429 and req["kind"] == "binance":
                    time.sleep(1.0)
                    resp = requests.get(req["url"], timeout=5)
                resp.raise_for_status()
                data = resp.json()
                if req["kind"] == "frankfurter":
                    rate = float(data["rates"][req["target"]])
                elif req["kind"] == "binance":
                    rate = float(data["price"])
            except Exception:
                rate = 1.0

        rates = np.full(2000000, rate, dtype=np.float64)
        mean_val = float(np.mean(rates))
        std_val = float(np.std(rates))
        
    print(time.time() - start)

if __name__ == '__main__':
    run_sequential_baseline()