from django.db import models
from django.contrib.auth.models import User
class Post(models.Model):
    """Model representing a post."""
    #postId       = models.AutoField(unique=True)
    metadata = models.CharField(max_length=300, help_text="Contain the data for the post.")
    user         = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    movie        = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=False, null=True)
    def __int__(self):
        return self.pk

class Rating(models.Model):
    id     = models.IntegerField(primary_key=True, unique=True)
    rating = models.IntegerField(help_text="Value from 0-5")
    comment      = models.CharField(max_length=300)
    post         = models.ForeignKey('Post', on_delete=models.RESTRICT, null=True) #Foregin key used because a rating can have one Post but a Post may have many ratings.
    #ratingUserId, this can be accessed via Post because post have a FK user
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __int__(self):
        return self.ratingId



class Role(models.Model):
    role         = models.CharField(max_length=16)
    User         = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.role





