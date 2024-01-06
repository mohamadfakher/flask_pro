from loguru import logger

def log_message(route):
    logger.info(f"route: '{route}'")