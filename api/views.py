from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from api.weather_providers import weather_api_provider

from .serializers import WeatherSettingSerializer, MessageSerializer
from .weather_setting_managers.factory import WeatherSettingManagerFactory
from .weather_providers.factory import WeatherProviderFactory
from .portal_providers.factory import PortalProviderFactory
from .models import Message
from .tasks import push_message_to_portal

class HelloAPIView(APIView):

    def get(self, _: Request) -> Response:
        weather_api_provider = WeatherProviderFactory.get_provider()
        data = weather_api_provider.get_from_settings()
        push_message_to_portal.delay()
        return Response({"message": "Message pushed to portal", "data": data})


class WeatherSettingAPIView(APIView):
    """
    GET  -> Get the current weather api polling settings
    PATCH -> Update the settings
    """

    def get(self, _: Request) -> Response:
        weather_setting_manager = WeatherSettingManagerFactory.get_manager()
        settings = weather_setting_manager.get_settings()
        serializer = WeatherSettingSerializer(instance=settings)
        return Response(serializer.data)

    def patch(self, request : Request) -> Response:
        serializer = WeatherSettingSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            weather_setting_manager = WeatherSettingManagerFactory.get_manager()
            updated = weather_setting_manager.update_settings(serializer.validated_data)
            serializer = WeatherSettingSerializer(instance=updated)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageListCreateView(ListCreateAPIView):
    """
    GET  -> List all messages stored locally
    POST -> Create new message, store locally, push to Portal API
    """

    queryset = Message.objects.all().order_by("-created_at")
    serializer_class = MessageSerializer

    def perform_create(self, serializer: MessageSerializer) -> None:
        # Save locally first
        message = serializer.save()
        portal_provider = PortalProviderFactory.get_provider()
        portal_response = portal_provider.push_message({"message": message.text})

        # Update local record with portal response
        message.delivered = portal_response["success"]
        message.portal_response = portal_response
        message.save(update_fields=["delivered", "portal_response"])
