from django.urls import path
from myapp.views import RegisterView, FileUploadView, FileListView, FileDetailView, FileDeleteView, FileUpdateView, FileDownloadView ,FileLinkView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns=[
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',TokenObtainPairView.as_view(),name='token_obtain'),
    path('refresh/',TokenRefreshView.as_view(),name="token_refresh"),
    #FILE CRUD
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('list/', FileListView.as_view(), name='file-list'),
    path('detail/<uuid:pk>/', FileDetailView.as_view(), name='file-detail'),
    path('delete/<uuid:pk>/', FileDeleteView.as_view(), name='file-delete'),
    path('update/<uuid:pk>/', FileUpdateView.as_view(), name='file-update'),
    #DOWNLOAD
    path('files/<uuid:pk>/get-link/', FileLinkView.as_view(), name='file-get-link'),
    path('download/<uuid:pk>/', FileDownloadView.as_view(), name='file-download'),
]