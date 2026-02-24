from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .services import AuthService
from .serializers import RegisterSerializer

class RegisterView(APIView):
    permission_classes=[AllowAny]

    def post (self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        clean_data = serializer.validated_data
        clean_data.pop('password_confirm', None)

        user=AuthService.register_user(clean_data)

        return Response({
            "status":"success",
            "message":f"User {user.first_name} created sucessfully.",
            "data":{
                "id":user.id,
                "email":user.email
            }
        },status=status.HTTP_201_CREATED)
