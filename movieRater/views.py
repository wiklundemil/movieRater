from urllib import request

from django.shortcuts import render
from django.http import HttpResponse

#For tmdb
import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

from .models import Post, User

import requests
from .serializers.serializers import PostSerializer, MovieSerializer


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

#Post methods
class CreatePost(generics.CreateAPIView):
    serializer_class = MovieSerializer
    queryset = Post.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract data from the serializer
        movie_id = serializer.validated_data['post_MovieId']
        metadata = serializer.validated_data['post_Metadata']
        user_id = serializer.validated_data['post_UserId']

        # Check if the user exists
        try:
            user = User.objects.get(userId=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=400)

        # Create the Post instance
        post_instance = Post.objects.create(
            postMovieId=movie_id,
            postMetadata=metadata,
            postUserId=user
            # You may need to set other fields as needed
        )

        # Return a response, you can customize this based on your needs
        return Response({'success': 'Post created successfully'}, status=201)




#Movie methods
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


@api_view(['GET'])
def searchMovieKey(request):
    query = request.query_params.get('query', '')
    if not query:
        return Response({'error': 'Missing query parameter'}, status=400)

    dataResponseFromTmdb = fetchDataFromTmdbTextSearch(query)
    return Response({'movie data for search': dataResponseFromTmdb})

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

#rating methods
def CreateRating(request):
    serializer = PostSerializer(data = request.data)

    if(serializer.is_valid()):
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
def searchPost(request):
    search_text = request.query_params.get('query', '')

    if not search_text:
        return Response({'error': 'Missing query parameter'}, status=400)

    matching_posts = Post.objects.filter(postMetadata=search_text)
    post_ids = [post.id for post in matching_posts]

    return Response({'matching_post_ids': post_ids})