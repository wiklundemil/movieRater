from django.contrib import admin
from django.urls import path
from . import views
from .views import postMovie

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', views.apiV1),
    path('api/post_movie/<str:query>/', postMovie, name='movie_text_search'),

]
