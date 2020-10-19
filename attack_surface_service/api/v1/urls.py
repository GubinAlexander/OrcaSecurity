from attack_surface_service.api.v1 import views
from django.urls import path, re_path

app_name = 'attack_surface_service'

urlpatterns = [
    re_path(r'^api/v1/attack$', views.AttackAPIView.as_view(), name='attack'),
    path('api/v1/stats/', views.StatsAPIView.as_view(), name='stats')
]
