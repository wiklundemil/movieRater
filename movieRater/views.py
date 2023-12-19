from urllib import request

from django.shortcuts import render
from django.http import HttpResponse

#For tmdb
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Post
import requests
from .serializers.serializers import PostSerializer, MovieSerializer, UserSerializer
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

#User views

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"token": "Password is invalid."}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_classes([SessionAuthentication])
def logout(request):
    try:
        request.auth.delete()
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
    except AttributeError:
        return Response({"detail": "Authentication failed. Unable to log out."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def validate(request):
    return Response("Token validated for {}".format(request.user.username))

#API
@api_view(['GET', 'POST'])
def apiV1(request):
    api_urls = {
        'Create':'/post-create/',
        'Read':'/post-read/',
        'Update':'/post-update/',
        'Delete':'/post-delete/',
    }
    return Response(api_urls)

#Post methods
@api_view(['GET'])
def searchPost(request):
    search_text = request.query_params.get('query', '')

    if not search_text:
        return Response({'error': 'Missing query parameter'}, status=400)

    matching_posts = Post.objects.filter(postMetadata=search_text)
    post_ids = [post.id for post in matching_posts]

    return Response({'matching_post_ids': post_ids})

#When creating a post this has to be done via postman
class CreatePost(generics.CreateAPIView):
    serializer_class = MovieSerializer
    queryset = Post.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        movie_query = request.data.get('moviequery', '')

        if not request.user.is_authenticated:
            return Response({'error': 'You have to be logged in as a user to make a post.'})

        movie_search_result = fetchDataFromTmdbTextSearch(movie_query)

        if not movie_search_result:
            return Response({'error':'No movie found for the search input'})

        movie_id    = movie_search_result[0]['id']
        movie_title = movie_search_result[0]['title']

        post_instance = Post.objects.create(
            movie=movie_id,
            metadata=movie_title,
            user=request.user
        )
        SendEmailUpdate(request, 'MOVIEEE TITLLLEEE')
        return Response({'success': 'Post created successfully'}, status=201)

class GetPostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


from rest_framework.response import Response
@api_view(['GET'])
def UpdatePost(request, post_id, newmovieid):
    postinstance = (Post.objects.get(id=post_id))
    response_from_movie = fetchMovieDataById(newmovieid)

    if not response_from_movie:
        return Response({'error': 'No movie found for the given id.'})
    else:
        if (request.user == postinstance.user):
            postinstance.movie = newmovieid
            postinstance.metadata = response_from_movie['title']
            postinstance.save()
        else:
            return Response({'error': 'You are not the author for this post.'})
    return Response(response_from_movie)

@api_view(['GET'])
def DeletePost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.user:
        post.delete()
        msg = 'Post ' + str(post_id) + ' deleted.'
        return Response({'success': msg})

    return Response({'error': 'You are not the author for this post.'})


#Movie methods
def fetchMovieDataById(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-Us'
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3NmI4NGFkODYyNDk4MTk5Y2Q2OTVjMGY1NGVmOWY0MSIsInN1YiI6IjY1NGRmOTRlMjg2NmZhMTA4ZGM0NmExMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.0t-keSrINdGSK_FTZNHY6VYDvHkRJWkYsa9o4u10weE"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        responseData = response.json()
        return {'id': responseData['id'], 'title': responseData['title']}
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

@api_view(['GET'])
def searchMovieKey(request):
    query = request.query_params.get('query', '')
    if not query:
        return Response({'error': 'Missing query parameter'}, status=400)

    dataResponseFromTmdb = fetchDataFromTmdbTextSearch(query)
    return Response({'movie data for search': dataResponseFromTmdb})

def fetchDataFromTmdbTextSearch(query):
    url = f"https://api.themoviedb.org/3/search/keyword?query={query}&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1OTIwZTEyY2ExOWViMzBjMDRmMWE0ZTc2ZWVjZWQ5YSIsInN1YiI6IjY1NGRmYTAyMjkzODM1NDNlZjUwMDE3MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.pH2bokeD4x33NfsKJaejV7HH__Y1yurQZ8QD4zPeN2Y"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        responseData = response.json()
        results = responseData.get('results', [])
        movies_info = [{'id': movie['id'], 'title' : movie['name'] } for movie in results]
        return movies_info
    else:
        return f"Error: {response.status_code} - {response.text}"

#rating methods
@api_view(['GET'])
def searchPost(request):
    search_text = request.query_params.get('query', '')

    if not search_text:
        return Response({'error': 'Missing query parameter'}, status=400)

    matching_posts = Post.objects.filter(metadata=search_text)
    post_ids = [post.id for post in matching_posts]

    return Response({'matching_post_ids': post_ids})

#Mail methods
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_classes([SessionAuthentication])
def uppvote(request, post_id, user_id):
    userId = request.user.id
    post = get_object_or_404(Post, pk=post_id)
    # Check if the user has upvoted the post
    has_upvoted = post.uppvotes.filter(pk=user_id).exists()
    if has_upvoted:
        post.uppvotes.remove(userId)
        return Response({'detail' : 'Upp vote has been cleared, a new vote can be cast'})
    else:
        post.uppvotes.add(userId)
        return Response({'details' : 'Upp vote successful'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_classes([SessionAuthentication])
def downvote(request, post_id, user_id):
    userId = request.user.id
    post = get_object_or_404(Post, pk = post_id)
    has_downvoted = post.downvotes.filter(pk=user_id).exists()
    if has_downvoted:
        post.downvotes.remove(userId)
        return Response({'detail' : 'Down vote has been cleared, a new vote can be cast'})
    else:
        post.downvotes.add(userId)
        return Response({'detail' : 'Down vote successful'})

def SendEmailUpdate(request, title):
    user = request.user.id
    template = render_to_string('emailtemplate.html', {'username': request.user, 'title': title})

    email = EmailMessage(
        'MovieRater following',
        template,
        settings.EMAIL_HOST_USER,
        [request.user.email],
    )
    email.fail_silently = True
    email.send()

    #raing = Rating.objects.get(id = user)
    context = {'detail': user}
    return Response({'sucess': 'Mail sent to, '+request.user.username+'!'})
