from src.logger.qa_logging.qa_logger import QALogger
import logging
import colorlog
import os

# Create the main logger instance
qa_logger = logging.getLogger("qa_logger")

# Set the logger level based on environment variable, or default to INFO
qa_logger.setLevel(os.getenv("QA_LOG_LEVEL", "INFO").upper())

# Define color scheme for different levels
log_colors = {
    'QUESTION': 'bold_blue',
    'ANSWER': 'bold_green',
    'INFO': 'white',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

# Create a colored formatter
formatter = colorlog.ColoredFormatter(
    fmt='%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
    log_colors=log_colors
)

# Create a stream handler and set the formatter
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Add the handler to the logger
qa_logger.addHandler(handler)
