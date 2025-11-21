from django.urls import path
from . import views

urlpatterns = [
    path('', views.usuarios_view, name='usuarios'),
    path('eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('creditos/', views.creditos_view, name='creditos'),
]