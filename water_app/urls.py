from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('api/', views.water_data_api, name='water_data_api'),
    path('', views.water_data_view, name='water_data_view'),
    path('chart_data/', views.chart_data, name='chart_data'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='water_app/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='water_app/logout.html'),name='logout'),

]
