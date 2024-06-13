# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.jira_login, name='jira_login'),
    path('callback/', views.jira_callback, name='jira_callback'),
    path('profile/', views.profile, name='profile'),
]
