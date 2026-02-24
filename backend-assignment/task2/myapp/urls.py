from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from myapp.views import RegisterView, AdditionView, SubtractionView ,DivisionView


urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',TokenObtainPairView.as_view(),name='token_obtain'),
    path('refresh/',TokenRefreshView.as_view(),name="token_refresh"),
    #ARITHMETIC OPERATIONS
    path('calculate/sum/<str:num1>/<str:num2>/',AdditionView.as_view(),name='add-operation'),
    path('calculate/difference/<str:num1>/<str:num2>/',SubtractionView.as_view(),name='sub-operation'),
    path('calculate/divide/<str:num1>/<str:num2>/',DivisionView.as_view(),name='div-operation'),
]