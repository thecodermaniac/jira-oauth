
# Create your views here.


# myapp/views.py

import requests
from requests_oauthlib import OAuth2Session
from django.shortcuts import redirect, render
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse

def jira_login(request):
    scope = ["read:me", "read:jira-user", "read:jira-work"]
    audience = "api.atlassian.com"

    jira_oauth = OAuth2Session(settings.JIRA_CLIENT_ID, scope=scope, redirect_uri=settings.JIRA_REDIRECT_URI)
    authorization_url, state = jira_oauth.authorization_url(
        settings.JIRA_AUTHORIZATION_BASE_URL,
        audience=audience,
    )
    request.session["oauth_state"] = state
    return redirect(authorization_url)

def jira_callback(request):
    jira_oauth = OAuth2Session(
        settings.JIRA_CLIENT_ID, state=request.session["oauth_state"], redirect_uri=settings.JIRA_REDIRECT_URI
    )
    token_json = jira_oauth.fetch_token(
        settings.JIRA_TOKEN_URL, client_secret=settings.JIRA_CLIENT_SECRET, authorization_response=request.build_absolute_uri()
    )
    return HttpResponse(f"Token: {token_json}<p />Projects: {', '.join(get_projects(token_json))}")

def get_projects(token_json):
    req = requests.get(
        "https://api.atlassian.com/oauth/token/accessible-resources",
        headers={
            "Authorization": f"Bearer {token_json['access_token']}",
            "Accept": "application/json",
        },
    )
    req.raise_for_status()
    resources = req.json()
    cloud_id = resources[0]["id"]

    oauth2_dict = {
        "client_id": settings.JIRA_CLIENT_ID,
        "token": {
            "access_token": token_json["access_token"],
            "token_type": "Bearer",
        },
    }
    jira = Jira(url=f"https://api.atlassian.com/ex/jira/{cloud_id}", oauth2=oauth2_dict)
    return [project["name"] for project in jira.projects()]