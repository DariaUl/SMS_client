import argparse
import sys
from src.config_loader import get_config
from src.logger import LOGGER
from src.sms_client import SMSClient


def get_parse():
    parser = argparse.ArgumentParser(description="CLI for sending SMS")
    parser.add_argument("sender", type=str, help="Sender number")
    parser.add_argument("recipient", type=str, help="Recipient number")
    parser.add_argument("message", type=str, help="Message text")
    
    return parser.parse_args()


def main():
    try:
        args = get_parse() 
        config = get_config()

        sms_service_url = config["sms_service_url"]
        host, port = sms_service_url.split(":")
        port = int(port.strip("/"))

        client = SMSClient(
            host=host,
            port=port,
            username=config["username"],
            password=config["password"]
        )

        response = client.send_sms(args.sender, args.recipient, args.message)

        print(f"Response Code: {response.status_code}")
        print(f"Response Body: {response.body}")

        LOGGER.info(f"Sent SMS: Sender={args.sender}, Recipient={args.recipient}, Message={args.message}")
        LOGGER.info(f"Response: Code={response.status_code}, Body={response.body}")

    except Exception as error:
        LOGGER.error(f"Ошибка: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()