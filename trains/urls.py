from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='trains/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('', views.ticket_list, name='ticket_list'), 
    path('ticket/new/', views.create_ticket, name='create_ticket'),
    path('ticket/<int:ticket_id>/trips/', views.manage_trips, name='manage_trips'),
]