from django.urls import path
from chat_messages import views

urlpatterns = [
    path('rooms/<slug>/messages/',views.MessageList.as_view()),
    
]