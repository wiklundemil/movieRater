from .models import Post
from django.contrib.auth.models import User
from rest_framework import serializers

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['postId', 'postMetadata'] #We can not use any fields connected to PK  because with HyperlinkedModelSerializer it brakes down because it dont want to show any PK
