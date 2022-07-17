from django.urls import path, re_path
from .views import homepage, HomePage, RegisterUser, LoginForm, logout_user, ListLink

urlpatterns = [
    path("", HomePage.as_view(), name="startpage"),
    path("login/", LoginForm.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
    path("registr/", RegisterUser.as_view(), name="registr"),
    path("link/", ListLink.as_view(), name="link"),
    path("<slug:slug>", homepage, name="redirect"),
  
]