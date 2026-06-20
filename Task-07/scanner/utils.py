import logging
import os
from urllib.parse import urlparse, urljoin
from collections import deque
import threading

# Thread-safe log buffer for real-time dashboard updates
LOG_BUFFER = deque(maxlen=200)
buffer_lock = threading.Lock()

class DashboardLogHandler(logging.Handler):
    """
    Custom logging handler that appends log messages to an in-memory buffer
    for the web interface.
    """
    def emit(self, record):
        try:
            msg = self.format(record)
            with buffer_lock:
                LOG_BUFFER.append(msg)
        except Exception:
            self.handleError(record)

def setup_logger(log_dir="logs", log_file="scanner.log"):
    """
    Configures and returns the logger, writing to both logs/scanner.log and console.
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger("VulnerabilityScanner")
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers if setup is called multiple times
    if logger.handlers:
        return logger

    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')

    # File Handler
    file_path = os.path.join(log_dir, log_file)
    file_handler = logging.FileHandler(file_path, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console Handler (Optional/optional console debug output)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Dashboard Buffer Handler
    buffer_handler = DashboardLogHandler()
    buffer_handler.setLevel(logging.DEBUG)
    buffer_handler.setFormatter(formatter)
    logger.addHandler(buffer_handler)

    return logger

def get_logs():
    """
    Retrieves the current buffered logs in a thread-safe manner.
    """
    with buffer_lock:
        return list(LOG_BUFFER)

def clear_logs():
    """
    Clears the log buffer.
    """
    with buffer_lock:
        LOG_BUFFER.clear()

def is_internal_url(url, base_url):
    """
    Checks if a URL belongs to the same domain/host as the base URL.
    """
    try:
        base_netloc = urlparse(base_url).netloc
        url_netloc = urlparse(url).netloc
        
        # If the URL is relative, netloc is empty, so it's internal
        if not url_netloc:
            return True
            
        return base_netloc == url_netloc
    except Exception:
        return False

def clean_url(url):
    """
    Cleans a URL by removing fragment identifiers and trailing slashes
    to prevent duplicate page scanning.
    """
    try:
        parsed = urlparse(url)
        # Remove fragments
        cleaned = parsed._replace(fragment="").geturl()
        if cleaned.endswith("/"):
            cleaned = cleaned[:-1]
        return cleaned
    except Exception:
        return url
