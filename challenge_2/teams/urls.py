from django.urls import path
from .views import TeamView, TeamView2

urlpatterns = [
    path('teams/', TeamView.as_view()),
    path('teams/<int:team_id>/', TeamView2.as_view())
]
