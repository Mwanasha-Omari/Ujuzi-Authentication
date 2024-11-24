from django.urls import path
from .views import UserListView, UserDetailView, RegisterView, LoginUser


urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'), 
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'), 
    path('register/', RegisterView.as_view(), name='register'),  # Endpoint for user registration
    path('users/', UserListView.as_view(), name='all_users'),
    path('user/login/', LoginUser.as_view(), name='login'), 
]
