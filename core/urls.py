from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('brand/<slug:slug>/', views.brand_detail, name='brand_detail'),
    path('room/<int:pk>/', views.room_detail, name='room_detail'),
    path('api/room/<int:pk>/availability/', views.check_availability, name='check_availability'),
    path('lien-he/', views.contact_view, name='contact'),
]
