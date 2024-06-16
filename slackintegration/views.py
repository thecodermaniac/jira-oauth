# myapp/views.py
from django.http import HttpResponse
from .slack_utils import send_slack_message,get_slack_user_details
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render
import requests
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse


def my_view(request):
    # Your view logic
    send_slack_message('#general', 'Hello from Django!')
    return HttpResponse("Message sent to Slack!")

@csrf_exempt
def slack_events(request):
    if request.method == 'POST':
        event_data = json.loads(request.body)
        if 'challenge' in event_data:
            return JsonResponse({"challenge": event_data['challenge']})

        if 'event' in event_data:
            event = event_data['event']
            if event['type'] == 'message' and  'subtype'not in event:
                # Handle message event
                channel = event['channel']
                user = event['user']
                text = event['text']
                send_slack_message(channel, f"Received message from <@{user}>: {text}")
                
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "not ok"})

def show_user_details(request, user_id):
    user_details = get_slack_user_details(user_id)
    if user_details:
        data = {
            'ok': True,
            'user': {
                'name': user_details['profile']['real_name'],
                'email': user_details['profile'].get('email', 'N/A'),  # Email may not be available
                'username': user_details['name'],
                'profile_image': user_details['profile']['image_192']
            }
        }
    else:
        data = {
            'ok': False,
            'error': 'User not found'
        }
    return JsonResponse(data)

# def slack_login(request):
#     slack_authorize_url = "https://slack.com/oauth/v2/authorize"
#     params = {
#         "client_id": settings.SLACK_CLIENT_ID,
#         "scope": "users:read users:read.email users.profile:read",  # Adjust scopes here
#         "redirect_uri": settings.SLACK_REDIRECT_URI,
#     }
#     url = f"{slack_authorize_url}?client_id={params['client_id']}&scope={params['scope']}&redirect_uri={params['redirect_uri']}"
#     return redirect(url)

def slack_login(request):
    slack_authorize_url = "https://slack.com/oauth/v2/authorize"
    scopes = "users.profile:read users:read users:read.email"  # Adjust scopes as needed
    redirect_uri = settings.SLACK_REDIRECT_URI
    client_id = settings.SLACK_CLIENT_ID
    
    # Redirect the user to Slack's OAuth page
    return redirect(f"{slack_authorize_url}?client_id={client_id}&scope={scopes}&redirect_uri={redirect_uri}")


def slack_callback(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponse("Authorization code not found.", status=400)

    # Exchange code for access token
    token_url = "https://slack.com/api/oauth.v2.access"
    response = requests.post(token_url, data={
        'client_id': settings.SLACK_CLIENT_ID,
        'client_secret': settings.SLACK_CLIENT_SECRET,
        'code': code,
        'redirect_uri': settings.SLACK_REDIRECT_URI,
    })
    response_data = response.json()
    if not response_data.get('ok'):
        error_message = response_data.get('error', 'Unknown error')
        return HttpResponse(f"Failed to authenticate with Slack. Error: {error_message}", status=400)

    # if response_data['token_type'] != 'user':
    #     return HttpResponse("Expected a user token but received a different token type.", status=400)

    user_id = response_data['authed_user']['id']
    user_details = get_slack_user_details(user_id)
    if user_details:
        data = {
            'ok': True,
            'user': {
                'name': user_details['profile']['real_name'],
                'email': user_details['profile'].get('email', 'N/A'),  # Email may not be available
                'username': user_details['name'],
                'profile_image': user_details['profile']['image_192']
            }
        }
    else:
        data = {
            'ok': False,
            'error': 'User not found'
        }
    return JsonResponse(data)
