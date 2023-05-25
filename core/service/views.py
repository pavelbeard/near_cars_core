from django.middleware.csrf import get_token

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf(request):
    """CSRF токен необходим для форм, написанных на фронте"""
    response = Response({"status": "the csrf cookie is set"}, status=status.HTTP_200_OK)
    response.set_cookie('csrftoken', get_token(request))
    return response
