from django.urls import path
from .views import stream_video

urlpatterns = [
    path('video/', stream_video),  # Correct path definition
]