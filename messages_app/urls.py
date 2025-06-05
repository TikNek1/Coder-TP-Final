from django.urls import path
from . import views
from .views import chat_with_user_redirect, conversation

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<str:username>/', conversation, name='conversation'),
    path("messages/start/", chat_with_user_redirect, name="chat_with_user_redirect"),
]