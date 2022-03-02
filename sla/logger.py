from loguru import logger
import sys

def formatter(record):
    return "{time} | {level} | {message}\n"

def logger_init(log_level:str,log_dest:str):
    logger.remove()
    if log_dest == 'stdout':
        log_dest = sys.stdout
    logger.add(log_dest, level=log_level, format=formatter, colorize=True)
  
LG = logger
