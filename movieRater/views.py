from urllib import request

from django.shortcuts import render
from django.http import HttpResponse

#For tmdb
import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from serializers import post_serializer
from rest_framework import generics

from .models import Post

import requests

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
    serializer_class = post_serializer

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
    return Response(api_urls)

@api_view(['POST', 'GET'])
def postMovie(request, query):
    dataResponseFromTmdb = fetchDataFromTmdbTextSearch(query)
    #return the data from TMDB
    return Response({'movie ID': dataResponseFromTmdb})

def fetchDataFromTmdbTextSearch(query):
    url = f"https://api.themoviedb.org/3/search/keyword?query={query}&page=1"
    #header containing jacomoel key
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1OTIwZTEyY2ExOWViMzBjMDRmMWE0ZTc2ZWVjZWQ5YSIsInN1YiI6IjY1NGRmYTAyMjkzODM1NDNlZjUwMDE3MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.pH2bokeD4x33NfsKJaejV7HH__Y1yurQZ8QD4zPeN2Y"
    }
    # make a response
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        responseData = response.json()
        results = responseData.get('results', [])
        movies_info = [{'id': movie['id'], 'name' : movie['name'] } for movie in results]
        return movies_info
    else:
        return f"Error: {response.status_code} - {response.text}"
