# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.slack_events, name='slack_events'),
    path('user/<str:user_id>/', views.show_user_details, name='show_user_details'),
    path('oauth/login/', views.slack_login, name='slack_login'),
    path('oauth/callback/', views.slack_callback, name='slack_callback'),
]
