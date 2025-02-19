from django.urls import path
from .views import ListView

urlpatterns = [
    path('', ListView.as_view(), name='lists'),
    path('<uuid:pk>/', ListView.as_view(), name='list_detail'),
]
