from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from accounts.serializers import UserRegisterSerializer
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from django.contrib.auth.password_validation import validate_password


User = get_user_model()


@api_view(['POST', ])
def register(request):
    if request.method == "POST":
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            data = {}
            user = serializer.save()
            data['response'] = "Successfully Created USER"
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def dashboard(request):
    if request.method == "POST":
        return Response({'response': "After Authentication"})
