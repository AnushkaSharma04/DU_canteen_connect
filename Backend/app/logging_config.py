import logging
import os

def setup_logging():
    """
    Configure logging with both console and file handlers.
    Logs will be saved inside 'logs/app.log'.
    """

    # Ensure logs directory exists
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "app.log")

    # Define log format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # File handler (writes logs to file)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)   # Log INFO and above to file

    # Console handler (prints logs to terminal)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)  # Log DEBUG and above to console

    # Root logger config
    logging.basicConfig(
        level=logging.DEBUG,  # Minimum level for root logger
        handlers=[file_handler, console_handler]
    )

    # Confirm setup
    logging.getLogger(__name__).info(f"Logging initialized. Logs will be saved to {log_file}")
