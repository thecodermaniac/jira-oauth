
# Create your views here.


# myapp/views.py

import requests
from requests_oauthlib import OAuth2Session
from django.shortcuts import redirect, render
from django.conf import settings

def jira_login(request):
    jira = OAuth2Session(
        settings.JIRA_CLIENT_ID,
        redirect_uri=settings.JIRA_REDIRECT_URI,
    )
    authorization_url, state = jira.authorization_url(settings.JIRA_AUTHORIZATION_BASE_URL)
    
    # Save the state in the session to validate the callback
    request.session['oauth_state'] = state
    return redirect(authorization_url)

def jira_callback(request):
    jira = OAuth2Session(
        settings.JIRA_CLIENT_ID,
        state=request.session['oauth_state'],
        redirect_uri=settings.JIRA_REDIRECT_URI,
    )
    token = jira.fetch_token(
        settings.JIRA_TOKEN_URL,
        client_secret=settings.JIRA_CLIENT_SECRET,
        authorization_response=request.build_absolute_uri()
    )

    # Save the token in the session or database as needed
    request.session['oauth_token'] = token

    return redirect('profile')

def profile(request):
    token = request.session.get('oauth_token')
    if not token:
        return redirect('jira_login')

    jira = OAuth2Session(settings.JIRA_CLIENT_ID, token=token)
    user_info = jira.get(settings.JIRA_API_BASE_URL + '/path_to_user_info_endpoint').json()

    return render(request, 'profile.html', {'user_info': user_info})

def jiraLol(request):
    
    return 'tytyy'