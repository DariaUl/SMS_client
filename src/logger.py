import logging

    
def setup_logger() -> logging.Logger: 
    logger = logging.getLogger("__name__")
    logger.setLevel(logging.DEBUG)
    
    file_handler = logging.FileHandler("logs/sms_client.log")
    file_handler.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    return logger

LOGGER: logging.Logger = setup_logger()