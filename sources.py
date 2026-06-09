def build_requests() -> list[dict]:
    reqs = []
    fx_pairs = [
        ("USD","EUR"), ("USD","GBP"), ("USD","JPY"), ("USD","CHF"),
        ("EUR","USD"), ("EUR","GBP"), ("EUR","JPY"), ("EUR","CHF"),
        ("GBP","USD"), ("GBP","EUR"), ("GBP","JPY"), ("GBP","CHF"),
        ("JPY","USD"), ("JPY","EUR"), ("JPY","GBP"), ("JPY","CHF"),
        ("CHF","USD"), ("CHF","EUR"), ("CHF","GBP"), ("CHF","JPY")
    ]
    for base, target in fx_pairs:
        reqs.append({
            "kind": "frankfurter",
            "url": f"https://api.frankfurter.app/latest?from={base}&to={target}",
            "pair": f"{base}/{target}",
            "base": base,
            "target": target,
            "cid": f"FX-{base}-{target}"
        })

    binance_symbols = [
        "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", 
        "ADAUSDT", "DOGEUSDT", "AVAXUSDT", "DOTUSDT", "LINKUSDT"
    ]
    for symbol in binance_symbols:
        reqs.append({
            "kind": "binance",
            "url": f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}",
            "pair": symbol,
            "base": symbol[:3],
            "target": symbol[3:],
            "cid": f"BN-{symbol}"
        })

    mock_pairs = [
        ("AUD","USD"), ("CAD","USD"), ("NZD","USD"), ("SGD","USD"),
        ("HKD","USD"), ("ZAR","USD"), ("TRY","USD"), ("MXN","USD"),
        ("BRL","USD"), ("INR","USD"), ("CNY","USD"), ("KRW","USD"),
        ("AUD","JPY"), ("CAD","JPY"), ("NZD","JPY"), ("SGD","JPY"),
        ("AUD","CAD"), ("AUD","NZD"), ("CAD","CHF"), ("NZD","CHF")
    ]
    for base, target in mock_pairs:
        reqs.append({
            "kind": "mock",
            "url": None,
            "pair": f"{base}/{target}",
            "base": base,
            "target": target,
            "cid": f"MOCK-{base}-{target}"
        })
    return reqs

ALL_REQUESTS = build_requests()