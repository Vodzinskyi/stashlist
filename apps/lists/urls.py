from django.urls import path
from . import views
from .views import ListView

urlpatterns = [
    path('lists/', ListView.as_view(), name='lists'),
    path('lists/<int:pk>/', ListView.as_view(), name='lists'),
]
