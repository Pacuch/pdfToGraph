import logging
from pathlib import Path

import colorlog
import os

# Create the main logger instance
document_logger = logging.getLogger("document_reading")

# Set logger level from environment variable or default to INFO
document_logger.setLevel(
    os.getenv("DOCUMENT_LOG_LEVEL", "INFO").upper()
)

# Avoid adding duplicate handlers if this module is imported multiple times
if not document_logger.handlers:
    # Define color scheme for console output
    log_colors = {
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }

    # Colored formatter for console
    color_formatter = colorlog.ColoredFormatter(
        fmt='%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
        log_colors=log_colors,
        style='%'
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(color_formatter)

    # File handler (plain text)
    log_file_path = os.getenv("DOCUMENT_LOG_FILE", Path("../logs/document_reading.log"))
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
    file_handler.setFormatter(file_formatter)

    # Add handlers
    document_logger.addHandler(console_handler)
    document_logger.addHandler(file_handler)

# Explicit export
__all__ = ["document_logger"]
