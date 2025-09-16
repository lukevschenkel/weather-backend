from django.urls import path
from .views import HelloAPIView, WeatherSettingAPIView, MessageListCreateView

urlpatterns = [
    path("hello/", HelloAPIView.as_view(), name="hello-world"),
    path("weather-setting/", WeatherSettingAPIView.as_view(), name="weather-setting"),
    path("message", MessageListCreateView.as_view(), name="message"),
]
