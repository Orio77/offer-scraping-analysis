import logging
import os
from datetime import datetime
import inspect # Added for contextual logging

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Generate log filename based on current date - this remains global for all loggers
LOG_FILENAME = datetime.now().strftime("%Y-%m-%d.log")
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILENAME)

def get_logger(name="offer_scraper", level=logging.INFO): # Default name for fallback or direct use
    """
    Configures and returns a logger instance.
    Logs to both console and a daily file.
    Ensures handlers are not duplicated for the same logger name.
    """
    logger = logging.getLogger(name)
    
    # If logger already has handlers, assume it's configured and return it.
    # This prevents adding duplicate handlers.
    if logger.hasHandlers():
        # Optionally, one could update the level of existing handlers here if needed,
        # but for simplicity, we assume level is set on first configuration.
        # logger.setLevel(level) # Ensure logger's effective level is set
        # for handler in logger.handlers:
        #    handler.setLevel(level)
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
    # All loggers configured by this function will write to the same daily file.
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
        # Cache logger instances once they are created for a specific name
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
            
            logger_name = "unknown_module" # Default/fallback
            if module:
                if module.__name__ == '__main__':
                    # For scripts run directly, use the filename without extension
                    filepath = frame.filename
                    logger_name = os.path.splitext(os.path.basename(filepath))[0]
                else:
                    logger_name = module.__name__
            
            if logger_name not in self._cached_loggers:
                # Get (and configure if new) a logger for this specific name.
                # The level will be the default from get_logger (e.g., INFO)
                self._cached_loggers[logger_name] = get_logger(logger_name)
            return self._cached_loggers[logger_name]
        except IndexError:
            # Fallback if stack inspection fails unexpectedly
            if "fallback_logger" not in self._cached_loggers:
                self._cached_loggers["fallback_logger"] = get_logger("fallback_logger")
            return self._cached_loggers["fallback_logger"]


    def __getattr__(self, name):
        # This is called for log.info, log.debug, log.exception etc.
        # It gets a logger contextual to the caller and returns the requested attribute (method).
        actual_logger = self._get_actual_logger()
        return getattr(actual_logger, name)

# Default logger for simple import: now uses the ContextualLogger
# This allows `from logger_config import log` to work as desired.
log = _ContextualLogger()