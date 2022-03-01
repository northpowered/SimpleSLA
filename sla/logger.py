from loguru import logger
import sys

LOG_DESTINATION = sys.stdout

def formatter(record):
    return "{time} | {level} | {message}\n"

def logger_init(log_level:str):
    logger.remove()
    logger.add(LOG_DESTINATION, level=log_level, format=formatter, colorize=True)

LG = logger
