from django.db import models
class Post(models.Model):
    """Model representing a post."""
    postId = models.IntegerField(max_length=11, unique=True)
    postMetadata = models.CharField(max_length=300, help_text="Contain the data for the post.")
    postUserId = models.ForeignKey('User', on_delete=models.RESTRICT, null=True)
    def __int__(self):
        return self.postId

class Rating(models.Model):
    ratingId = models.IntegerField(max_length=11, unique=True)
    ratingRating = models.IntegerField(max_length=2, help_text="Value from 0-5")
    ratingComment = models.CharField(max_length=300)
    ratingPost = models.ForeignKey('Post', on_delete=models.RESTRICT, null=True) #Foregin key used beacuse a rating can have one Post but a Post may have many ratings.
    #ratingUserId, this can be accessed via Post beacuse post have a FK user

    def __int__(self):
        return self.ratingId



#APIS






