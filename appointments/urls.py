from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_panel, name='user_panel'),
    path('user/', views.user_panel, name='user_panel'),
    path('admin123/', views.admin_panel, name='admin_panel'),
    path('edit/<int:pk>/', views.edit_appointment, name='edit_appointment'),
    path('success/', views.success, name='success'),
    path('add_mechanic/', views.add_mechanic, name='add_mechanic'), 
    path('delete_appointment/<int:pk>/', views.delete_appointment, name='delete_appointment'),
    path('remove_mechanic/<int:pk>/', views.remove_mechanic, name='remove_mechanic'),  
    
]