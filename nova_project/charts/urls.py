from django.urls import path

from .import views

app_name = 'charts'

urlpatterns = [
    path('analysis/', views.data_analysis, name='data_analysis'),
]