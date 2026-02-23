from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegistrationSerializer,UserFileSerializer
from .services import AuthService, FileStorageService
from django.shortcuts import get_object_or_404
from .models import UserFile
from rest_framework.exceptions import ValidationError

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

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        files = request.FILES.getlist('file')
        if not files:
            return Response({"error": "No files uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_records = []
        errors = []
        for file_obj in files:
            try:
                new_file = FileStorageService.process_and_store_file(
                    user=request.user, 
                    file_obj=file_obj, 
                    data=request.data
                )
                uploaded_records.append(new_file)
            except Exception as e:
                errors.append({file_obj.name: str(e)})
        serializer = UserFileSerializer(uploaded_records, many=True)
        return Response({
            "uploaded": serializer.data,
            "errors": errors
        }, status=status.HTTP_201_CREATED if uploaded_records else status.HTTP_400_BAD_REQUEST)


class FileListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        files = UserFile.objects.filter(owner=request.user, is_archived=False)
        serializer = UserFileSerializer(files, many=True)
        return Response(serializer.data)

class FileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        file_instance = get_object_or_404(UserFile, pk=pk, owner=request.user, is_archived=False)
        serializer = UserFileSerializer(file_instance)
        return Response(serializer.data)

class FileDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        file_instance = get_object_or_404(UserFile, pk=pk, owner=request.user, is_archived=False)
        file_instance.is_archived = True
        file_instance.save()
        return Response({"status": "File Soft Deleted"}, status=status.HTTP_200_OK)
    
class FileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        file_instance = get_object_or_404(UserFile, pk=pk, owner=request.user)
    
        new_file = request.FILES.get('file')

        try:
            updated_file = FileStorageService.update_file_record(
                file_instance=file_instance,
                data=request.data,
                new_file_obj=new_file
            )
            
            serializer = UserFileSerializer(updated_file)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)