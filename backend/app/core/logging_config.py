import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from pythonjsonlogger.jsonlogger import JsonFormatter  # Correct import

def setup_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.handlers.clear()

    log_format = '%(asctime)s %(levelname)s %(name)s %(message)s'
    formatter = JsonFormatter(log_format)  # Correct usage

    # Ensure logs/ directory exists
    log_dir = "backend/logs"
    os.makedirs(log_dir, exist_ok=True)

    # Console (stdout) handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler with rotation
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "app.log"),
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Optional: quiet down noisy loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
