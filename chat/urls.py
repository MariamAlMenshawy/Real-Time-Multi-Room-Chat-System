from django.urls import path
from chat import views

urlpatterns = [
    path('rooms/',views.RoomList.as_view()),
    path('rooms/<slug>/',views.Room_slug.as_view()),
    path('new_room/',views.PostRoom.as_view()),
    

]