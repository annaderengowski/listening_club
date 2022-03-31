from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('random_album.urls')),
    path('accounts/login/', auth_views.login, name='login'),
    path('accounts/logout/', auth_views.login, name='logout'),
]
