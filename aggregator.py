import asyncio
import aiohttp
import random
from sources import ALL_REQUESTS
from processor import process_data

async def fetch(session, req, logger):
    logger.info("Fetching", extra={'cid': req['cid']})
    if req["kind"] == "mock":
        await asyncio.sleep(random.uniform(0.1, 0.5))
        req["rate"] = random.uniform(0.5, 150.0)
        return req

    for attempt in range(3):
        try:
            async with session.get(req["url"], timeout=5) as resp:
                if resp.status == 429 and req["kind"] == "binance":
                    await asyncio.sleep(1.0 * (attempt + 1))
                    continue
                resp.raise_for_status()
                data = await resp.json()
                if req["kind"] == "frankfurter":
                    req["rate"] = float(data["rates"][req["target"]])
                elif req["kind"] == "binance":
                    req["rate"] = float(data["price"])
                return req
        except Exception:
            if attempt == 2:
                req["rate"] = 1.0
                return req
            await asyncio.sleep(1.0 * (attempt + 1))

async def collector(async_q, logger):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, req, logger) for req in ALL_REQUESTS]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for res in results:
            if isinstance(res, dict):
                await async_q.put(res)
    await async_q.put(None)

async def dispatcher(async_q, mp_q, ppe):
    loop = asyncio.get_running_loop()
    while True:
        data = await async_q.get()
        if data is None:
            mp_q.put(None)
            break
        result = await loop.run_in_executor(ppe, process_data, data)
        mp_q.put(result)