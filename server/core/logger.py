import os
import logging

def logging_config():
    log_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs', 'server.log'))

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )
    
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    return logger