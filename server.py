import asyncio
import logging

import commons

logger = logging.getLogger(__name__)


async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    try:
        while True:
            data = await reader.read(100)
            if not data:
                logger.info("connection closed by peer")
                break
            writer.write(data)
            await writer.drain()
    except Exception:
        logger.exception("unexpected error")
    finally:
        writer.close()
        await writer.wait_closed()


async def main() -> None:
    commons.config_logger()
    server = await asyncio.start_server(handle, commons.SERVER_HOST, commons.SERVER_PORT)

    address = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    logger.info(f"Serving on {address}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
