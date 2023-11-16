from urllib import request

from django.shortcuts import render
from django.http import HttpResponse

#For tmdb
import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .serializers import PostSerializer
from rest_framework import generics

from .models import Post

@api_view(['GET', 'POST'])
def apiV1(request):
    api_urls = {
        'Create':'/post-create/',
        'Read':'/post-read/',
        'Update':'/post-update/',
        'Delete':'/post-delete/',
    }
    return Response(api_urls)

class GetPostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

@api_view(['GET'])
def GetMovie(request, movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-Us'

   # url = "https://api.themoviedb.org/3/movie/872585?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3NmI4NGFkODYyNDk4MTk5Y2Q2OTVjMGY1NGVmOWY0MSIsInN1YiI6IjY1NGRmOTRlMjg2NmZhMTA4ZGM0NmExMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.0t-keSrINdGSK_FTZNHY6VYDvHkRJWkYsa9o4u10weE"
    }

    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
        return Response(data)
    else:
        # If the request was not successful, return an error response
        return Response({"error": "Failed to retrieve movie details"}, status=response.status_code)