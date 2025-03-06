import argparse
import base64
from logger import LOGGER, mask_phone_number
from config_loader import get_config
from sms_client import Request

def parse_args():
    parser = argparse.ArgumentParser(description="CLI SMS Sender")
    parser.add_argument("--from", required=True, dest="sender", help="Sender phone number")
    parser.add_argument("--to", required=True, dest="recipient", help="Recipient phone number")
    parser.add_argument("--text", required=True, dest="message", help="Message text")
    return parser.parse_args()


def send_sms(config, sender, recipient, message):
    url = f"{config['base_url']}/send_sms"
    auth = f"{config['username']}:{config['password']}"
    auth_header = f"Basic {base64.b64encode(auth.encode()).decode()}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": auth_header
    }
    body = {
        "from": sender,
        "to": recipient,
        "text": message
    }

    request = Request("POST", url, headers=headers, body=body)
    try:
        response = request.send()
        masked_sender = mask_phone_number(sender)
        masked_recipient = mask_phone_number(recipient)

        LOGGER.info(f"Sent SMS: From={masked_sender}, To={masked_recipient}, Message={message}")
        LOGGER.info(f"Response: Status Code={response.status_code}, Body={response.body}")

        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.body}")
    except Exception as error:
        LOGGER.error(f"An error occurred: {error}")
        print(f"Error: {error}")


if __name__ == "__main__":
    args = parse_args()
    config = get_config("config.toml")

    try:
        send_sms(config, args.sender, args.recipient, args.message)
    except Exception as error:
        LOGGER.error(f"Failed to send SMS: {error}")
        print(f"Error: {error}")