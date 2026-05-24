from django.urls import path
from .import views

app_name = 'f1_project'

urlpatterns = [
    path('standings/', views.season_standings, name='season_standings'),
    path('results/', views.season_results, name='season_results'),
    path('teams-and-drivers/', views.teams_and_drivers_list, name='teams-and-drivers'),
]