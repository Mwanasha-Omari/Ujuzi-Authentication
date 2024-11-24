from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("callback/", views.callback, name="callback"),
]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('login/', views.login, name='login'),
#     path('logout/', views.logout, name='logout'),
#     path('auth/callback/', views.callback, name='callback'),
#     path('auth/', views.auth_handler, name='auth_handler'),  # New endpoint for postman
# ]



