from django.contrib import admin
from django.urls import path
from . import views
from .views import  searchMovieKey

urlpatterns = [
    path('admin/',    admin.site.urls),
    path('api/',      views.apiV1,       name="api-overview"),

    #path('api/readmovie/id=<int:movie_id>/',  views.GetMovie, name='get_movie_by_id'),
    path('api/searchmovie/', searchMovieKey, name='tmdb_key_textsearch'),

    path('api/postlist/',   views.GetPostList.as_view(), name='post_list'),
    path('api/createpost/', views.CreatePost.as_view(), name='create_post'),
    path('api/searchpost/', views.searchPost, name='search_user_posts'),
    path('api/updatepost/id=<int:post_id>&newmovieid=<int:newmovieid>/', views.UpdatePost, name='update_post'),
    path('api/deletepost/id=<int:post_id>', views.DeletePost, name='delete_post'),

    path('api/signup/',   views.signup, name='signup'),
    path('api/logout/',   views.logout, name='logout'),
    path('api/login/',    views.login, name='login'),
    path('api/validate/', views.validate, name='validate_token'),

    path('api/rate/', views.createRating, name='rate'),

]
