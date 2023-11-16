from django.contrib import admin
from django.urls import path
from . import views
from .views import postMovie

urlpatterns = [
    path('admin/',    admin.site.urls),
    path('api/',      views.apiV1,       name="api-overview"),
    path('postList/', views.GetPostList.as_view(), name='post_list'),
    path('movie/id=<int:movie_id>/', views.GetMovie, name='get_movie_by_id'),
    path('api/post_movie/<str:query>/', postMovie, name='movie_text_search'),

]
