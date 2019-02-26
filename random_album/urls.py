from django.urls import path

from random_album import views
from random_album.views import AlbumListView, RandomAlbumView

urlpatterns = [
    path('', views.index, name='index'),
    path('album_list/', AlbumListView.as_view(), name='album-list'),
    path('random_album/', RandomAlbumView.as_view(), name='random-album'),
]