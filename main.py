import asyncio
import multiprocessing
import logging
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from aggregator import collector, dispatcher
from storage import init_db, save_to_db

class CIDFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, 'cid'):
            record.cid = 'SYS'
        return True

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(processName)s] [%(threadName)s] [%(cid)s] %(message)s'
)
logger = logging.getLogger(__name__)
logger.addFilter(CIDFilter())

def db_writer(mp_q):
    while True:
        data = mp_q.get()
        if data is None:
            break
        save_to_db(data)
        logger.info("Saved", extra={'cid': data['cid']})

async def main():
    init_db()
    async_q = asyncio.Queue()
    mp_q = multiprocessing.Queue()

    ppe = ProcessPoolExecutor()
    tpe = ThreadPoolExecutor()
    loop = asyncio.get_running_loop()

    db_task = loop.run_in_executor(tpe, db_writer, mp_q)
    col_task = asyncio.create_task(collector(async_q, logger))
    disp_task = asyncio.create_task(dispatcher(async_q, mp_q, ppe))

    try:
        await asyncio.gather(col_task, disp_task)
        await db_task
    except (asyncio.CancelledError, KeyboardInterrupt):
        pass
    finally:
        ppe.shutdown(wait=False, cancel_futures=True)
        tpe.shutdown(wait=False, cancel_futures=True)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass