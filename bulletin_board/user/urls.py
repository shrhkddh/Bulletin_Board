from django.urls import path

from .views import (
    UserSignUpView,
    UserSignInView
)

urlpatterns = [
    path('/sign-up', UserSignUpView.as_view()),
    path('/sign-in', UserSignInView.as_view()),
]