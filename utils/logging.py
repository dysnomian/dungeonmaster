import logging
import sys

logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.dialects").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.dialects").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the logger's log level to DEBUG

# Create a handler for stdout
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.WARNING)  # Set the handler's log level to WARNING

# Create a handler for the file
file_handler = logging.FileHandler("dm.log")
file_handler.setLevel(logging.INFO)  # Set the handler's log level to INFO

# Add the handlers to the logger
logger.addHandler(stdout_handler)
logger.addHandler(file_handler)

# Test the logger
logger.info("This will go to the file.")
logger.warning("This will go to stdout and the file.")

logger.debug("Logger initialized.")
