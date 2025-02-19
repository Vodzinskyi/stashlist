from django.contrib import admin
from django.urls import path, include

from apps.media_items.views import MediaItemView
from apps.users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('register/', views.create_user, name='create_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('lists/', include('apps.lists.urls')),
    path('lists/<uuid:list_id>/media-items/<uuid:pk>/', MediaItemView.as_view(), name='media_item'),
]
