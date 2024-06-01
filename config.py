import logging

def setup_logging():
    """Configures application-wide logging."""
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
