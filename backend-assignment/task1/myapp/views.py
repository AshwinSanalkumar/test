from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer
from .services import AuthService

class RegisterView(APIView):
    permission_classes=[AllowAny]

    def post (self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user=AuthService.register_user(serializer.validated_data)

        return Response({
            "status":"success",
            "message":f"User {user.first_name} created sucessfully.",
            "data":{
                "id":user.id,
                "email":user.email
            }
        },status=status.HTTP_201_CREATED)