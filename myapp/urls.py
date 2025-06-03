from django.urls import path
from .views import stream_video, list_files

urlpatterns = [
    path('video/<str:filename>/', stream_video, name='stream_video'),
    path('list-files/', list_files, name='list_files'),

]