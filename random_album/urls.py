from django.urls import path

from random_album import views
from random_album.views import AlbumListView

urlpatterns = [
    path('', views.index, name='index'),
    path('album_list/', AlbumListView.as_view(), name='album-list'),
]