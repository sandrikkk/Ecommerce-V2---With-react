from django.urls import path
from product.views import user_views as views


urlpatterns = [
    path('', views.GetUsers.as_view()),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', views.GetUserProfile.as_view()),
    path('register/', views.RegisterUser.as_view(), name = 'register'),
]
    