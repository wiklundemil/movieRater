from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

import requests

@api_view(['GET', 'POST'])
def apiV1(request):
    api_urls = {
        'Create':'/user-create/',
        'Read':'/user-read/',
        'Update':'/user-update/',
        'Delete':'/user-delete/',
    }
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

