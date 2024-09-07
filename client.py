import asyncio
import logging
import random

import commons
from database import Database

logger = logging.getLogger(__name__)

MESSAGE = "Ping"
MESSAGE_COUNT = 5
DB_FILENAME = "dbsqlite.db"


async def subprogram(message: str, task_id: int, db: Database) -> None:
    reader, writer = await asyncio.open_connection(commons.SERVER_HOST, commons.SERVER_PORT)
    try:
        logger.info(f"task {task_id} started")
        for i in range(1, MESSAGE_COUNT + 1):
            writer.write(message.encode())
            await writer.drain()

            data = await reader.read(100)
            logger.info(f"task {task_id} received: {data}, message № {i}")
            db.save_message(data.decode())
            if i < MESSAGE_COUNT:
                await asyncio.sleep(random.randint(5, 10))
    except Exception:
        logger.exception("unexpected error")
    finally:
        logger.info(f"task {task_id} finished")
        writer.close()
        await writer.wait_closed()


async def main() -> None:
    commons.config_logger()
    db = Database(DB_FILENAME)
    db.create_table()
    tasks = []
    for i in range(1, 11):
        tasks.append(asyncio.create_task(subprogram(MESSAGE, i, db)))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
