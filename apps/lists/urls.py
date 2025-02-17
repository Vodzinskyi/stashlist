from django.urls import path
from . import views

urlpatterns = [
    path('add-list/', views.add_list, name='add_list'),
]
