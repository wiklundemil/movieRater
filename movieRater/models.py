from django.db import models


class Post(models.Model):
    """Model representing a post."""
    postId       = models.IntegerField(unique=True)
    postMetadata = models.CharField(max_length=300, help_text="Contain the data for the post.")
    postUserId   = models.ForeignKey('User', on_delete=models.RESTRICT, null=True)
    postMovieId  = models.IntegerField(unique=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=False, null=True)
    def __int__(self):
        return self.postId

class Rating(models.Model):
    ratingId      = models.IntegerField(unique=True)
    ratingRating  = models.IntegerField(help_text="Value from 0-5")
    ratingComment = models.CharField(max_length=300)
    ratingPost    = models.ForeignKey('Post', on_delete=models.RESTRICT, null=True) #Foregin key used because a rating can have one Post but a Post may have many ratings.
    #ratingUserId, this can be accessed via Post because post have a FK user
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __int__(self):
        return self.ratingId

class User(models.Model):
    userId       = models.IntegerField(unique=True)
    userName     = models.CharField(max_length=28)
    userSurname  = models.CharField(max_length=28)
    userForename = models.CharField(max_length=28)
    userFavGenre = models.CharField(max_length=28, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __int__(self):
        return self.userName

class Role(models.Model):
    role       = models.CharField(max_length=16)
    roleUserId = models.ForeignKey('User', on_delete=models.RESTRICT, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.role

#class Following(models.Model):
    #userId    = models.ForeignKey('User', on_delete=models.RESTRICT, null=True)
    #following = models.ForeignKey('User', on_delete=models.RESTRICT, null=True)



#APIS






