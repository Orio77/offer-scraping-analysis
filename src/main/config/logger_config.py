import logging
import os
from datetime import datetime
import inspect 

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILENAME = datetime.now().strftime("%Y-%m-%d.log")
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILENAME)

def get_logger(name="offer_scraper", level=logging.INFO): 
    logger = logging.getLogger(name)
    
    if logger.hasHandlers():
        return logger
        
    logger.setLevel(level)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console Handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File Handler - daily log files
    fh = logging.FileHandler(LOG_FILE_PATH, mode='a', encoding='utf-8')
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    return logger

class _ContextualLogger:
    """
    A logger proxy that determines the calling module's name for each log operation.
    """
    def __init__(self):
        self._cached_loggers = {}

    def _get_actual_logger(self):
        """
        Determines the caller's module and returns an appropriately named logger.
        inspect.stack()[0] is _get_actual_logger
        inspect.stack()[1] is the __getattr__ call (e.g., log.info)
        inspect.stack()[2] is the user's code that called log.info()
        """
        try:
            frame = inspect.stack()[2]
            module = inspect.getmodule(frame[0])
            
            logger_name = "unknown_module" # fallback
            if module:
                if module.__name__ == '__main__':
                    filepath = frame.filename
                    logger_name = os.path.splitext(os.path.basename(filepath))[0]
                else:
                    logger_name = module.__name__
            
            if logger_name not in self._cached_loggers:
                self._cached_loggers[logger_name] = get_logger(logger_name)
            return self._cached_loggers[logger_name]
        except IndexError:
            # Fallback if stack inspection fails unexpectedly
            if "fallback_logger" not in self._cached_loggers:
                self._cached_loggers["fallback_logger"] = get_logger("fallback_logger")
            return self._cached_loggers["fallback_logger"]


    def __getattr__(self, name):
        actual_logger = self._get_actual_logger()
        return getattr(actual_logger, name)

log = _ContextualLogger()