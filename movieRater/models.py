from django.db import models
from django.contrib.auth.models import User
class Post(models.Model):

    """Model representing a post."""
    #postId       = models.AutoField(unique=True)
    metadata     = models.CharField(max_length=300, help_text="Contain the data for the post.")
    user         = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    uppvotes     = models.ManyToManyField(User, related_name='uppvotedposts')
    downvotes    = models.ManyToManyField(User, related_name='downvotedposts')
    movie        = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
   # slug         = models.SlugField(max_length=255, unique=True, blank=False, null=True)
    def __int__(self):
        return self.pk


