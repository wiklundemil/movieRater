from ..models import Post
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Post
        fields = ['id', 'metadata', 'user'] #We can not use any fields connected to PK  because with HyperlinkedModelSerializer it brakes down because it dont want to show any PK

class MovieSerializer(serializers.HyperlinkedModelSerializer):
    # These are connected to the fields which is also make up the form in rest framework.
    post_MovieId  = serializers.CharField(max_length=100)
    post_Metadata = serializers.CharField(max_length=100)
    post_UserId   = serializers.CharField(max_length=100)
    class Meta:
        model = Post
        fields = ['post_MovieId', 'post_Metadata', 'post_UserId']


# class RatingSerializer(serializers.HyperlinkedModelSerializer):
#     id = serializers.IntegerField()
#     rating = serializers.IntegerField()
#
#     class Meta:
#         model = Rating
#         fields = ['id', 'rating']


