import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import os
import multiprocessing as mp

import aiecommon.custom_logger as custom_logger
logger = custom_logger.get_logger()

AIENERGY_MAX_WORKERS=os.getenv("AIENERGY_MAX_WORKERS")

def start_process_pool_executor(app, max_workers = None, multiprocessing_method = None):

    app.state.max_workers = max_workers if max_workers else int(AIENERGY_MAX_WORKERS) if AIENERGY_MAX_WORKERS else os.cpu_count()

    logger.info(f"Starting proces pool executor, max_workers={app.state.max_workers}, cpu_count={os.cpu_count()}")


    if not multiprocessing_method:
        multiprocessing_method = os.getenv("AIENERGY_MULTIPROCESSING_METHOD", "fork")
    # forkserver

    mp_fork_context = mp.get_context(multiprocessing_method)

    # app.state.executor = ThreadPoolExecutor(
    return ProcessPoolExecutor(
        max_workers=app.state.max_workers,
        # max_tasks_per_child=1,
        mp_context=mp_fork_context
    )

async def restart_process_pool_executor(app):

    new_executor = start_process_pool_executor()

    async with app.state.swap_lock:
        old_executor = app.state.executor
        app.state.executor = new_executor

    await asyncio.to_thread(old_executor.shutdown, wait=True, cancel_futures=False)
