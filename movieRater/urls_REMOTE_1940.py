from django.contrib import admin
from django.urls import path
from . import views
from .views import  searchMovieKey

urlpatterns = [
    path('admin/',    admin.site.urls),
    path('api/',      views.apiV1,       name="api-overview"),
    path('api/postlist/', views.GetPostList.as_view(), name='post_list'),
    path('api/readmovie/id=<int:movie_id>/',  views.GetMovie, name='get_movie_by_id'),
    path('api/createpost/', views.CreatePost, name='create_post'),
    path('api/searchmovie/', searchMovieKey, name='tmdb_key_textsearch'),

    path('api/searchpost/', views.searchPost, name='search_user_posts'),
]
