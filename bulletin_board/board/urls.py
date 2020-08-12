from django.urls import path

from .views import (
    BoardView,
    BoardListView
)

urlpatterns = [
    path('/posting', BoardView.as_view()),
    path('/boardlist', BoardListView.as_view())
]