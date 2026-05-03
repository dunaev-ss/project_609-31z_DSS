from django.urls import path
from . import views

app_name = 'f1_project'

urlpatterns = [
    path('calendar/', views.calendar_view, name='calendar'),
    path('standings/', views.season_standings, name='season_standings'),
    path('results/', views.season_results, name='season_results'),
    path('teams/', views.teams_list, name='teams'),
    path('drivers/', views.drivers_list, name='drivers'),
    path('analysis/', views.data_analysis, name='data_analysis'),
]