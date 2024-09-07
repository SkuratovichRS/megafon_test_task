import logging

logger = logging.getLogger(__name__)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000


def config_logger() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s; %(message)s")
    logger.info("logger configured")
