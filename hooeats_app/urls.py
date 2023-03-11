from django.urls import path
from .views import views
from .views import auth

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", auth.signup, name="signup"),
    path("handle-signup", auth.handle_signup, name="handle_signup"),
    path("api/signup-valid", auth.signup_valid, name="signup_valid")
]