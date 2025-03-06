import logging
import os


def setup_logger() -> logging.Logger:
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logger = logging.getLogger("sms_client")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("logs/sms_client.log")
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger

LOGGER = setup_logger()

def mask_phone_number(phone: str) -> str:
    return f"{phone[:3]}-XXX-{phone[-4:]}"