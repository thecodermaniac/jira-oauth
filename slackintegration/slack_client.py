# myapp/slack_client.py
from slack_sdk import WebClient
from django.conf import settings

slack_client = WebClient(token=settings.SLACK_TOKEN)
