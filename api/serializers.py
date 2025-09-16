from rest_framework import serializers
from .models import Message


class WeatherSettingSerializer(serializers.Serializer):
    zip_code = serializers.CharField(max_length=10)
    mode = serializers.ChoiceField(choices=["current", "forecast"])
    forecast_days = serializers.IntegerField()
    weather_api = serializers.ChoiceField(choices=["weatherapi", "dummy", "openweathermap"])


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "text", "created_at", "delivered", "portal_response"]
