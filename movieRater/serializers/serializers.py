from django.contrib.auth.models import User
from rest_framework import serializers

class userSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['userName', 'userSurname', 'userForename', 'userFavGenre']


