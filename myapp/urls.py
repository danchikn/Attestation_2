from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('register/', views.register, name='register'),
    path('export/', views.export_csv, name='export_csv'),
]
