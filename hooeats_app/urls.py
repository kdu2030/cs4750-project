from django.urls import path
from .views import views
from .views import auth

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", auth.signup, name="signup"),
    path("signin", auth.signin, name="signin"),
    path("signout", auth.signout, name="signout"),
    path("signin/<str:error>/", auth.signin_error, name="signin_error"),
    path("signup/<str:error>/", auth.signup_error, name="signup_error"),
    path("handle-signin", auth.handle_signin, name="handle_signin"),
    path("handle-signup", auth.handle_signup, name="handle_signup"),
    path("api/signup-valid", auth.signup_valid, name="signup_valid")
]