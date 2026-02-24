from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .services import AuthService, ArithmeticService
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
    
class AdditionView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,num1,num2):
        result= ArithmeticService.add(num1,num2)

        if result is None:
            return Response(
                {"error":"Invalid Input. Both parameters must be numbers."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            "operation": "sum",
            "result": result
        }, status=status.HTTP_200_OK)

class SubtractionView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,num1,num2):
        result= ArithmeticService.difference(num1,num2)

        if result is None:
            return Response(
                {"error":"Invalid Input. Both parameters must be numbers."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({
            "operation": "difference",
            "result": result
        }, status=status.HTTP_200_OK)
    
class DivisionView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,num1,num2):
        result= ArithmeticService.quotient(num1,num2)

        if result is None:
            if str(num2) == "0":
                 return Response({"error": "Division by zero is not allowed."}, status=status.HTTP_400_BAD_REQUEST)
            return Response(
                {"error":"Invalid Input. Both parameters must be numbers."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({
            "operation": "Division",
            "result": result
        }, status=status.HTTP_200_OK)
    
class MultiplicationView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,num1,num2):
        result= ArithmeticService.product(num1,num2)

        if result is None:
            return Response(
                {"error":"Invalid Input. Both parameters must be numbers."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({
            "operation": "multiplication",
            "result": result
        }, status=status.HTTP_200_OK)