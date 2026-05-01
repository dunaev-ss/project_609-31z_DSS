from django.urls import path

from . import views

app_name = 'f1_project'

urlpatterns = [
    path('results/', views.season_results, name='season_results'),
]