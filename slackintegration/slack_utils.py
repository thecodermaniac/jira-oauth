# myapp/slack_utils.py
from .slack_client import slack_client

def send_slack_message(channel, text):
    response = slack_client.chat_postMessage(
        channel=channel,
        text=text
    )
    return response

def get_slack_user_details(user_id):
    response = slack_client.users_info(user=user_id)
    if response["ok"]:
        return response["user"]
    return None