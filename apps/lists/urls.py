from django.urls import path
from .views import ListView, ListDetailView

urlpatterns = [
    path('', ListView.as_view(), name='lists'),
    path('<uuid:pk>/', ListDetailView.as_view(), name='list_detail'),
]
