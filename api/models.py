from django.db import models
from django.contrib.auth.models import User
#from django.core.validators import MaxValueValidator, MinValueValidator


# Allow me to explain:
# Using the django.contrib.auth.models import, I can obtain
# a user model that is already built by Django. Based on this,
# I have created the Favorite model which references one movie and one
# user. This is the model which stores users favorite movies.
# The Movie model is relatively straightforward.

class Movie(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360, blank=True)

    def no_of_favorites(self):
        favorites = Favorite.objects.filter(movie=self)
        return len(favorites)

class Favorite(models.Model):
    # When we remove a movie or a user, we need to also remove
    # the favorites saved for that movie to ensure DB is not
    # keeping favorites for movies/users that no longer exist.

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def my_favorites(self):
        favorites = Favorite.objects.filter(user=self.user)
        return favorites

    class Meta:
        # Unique together ensures that users cannot favorite
        # the same movie twice, and vice versa, as in the movie
        # cannot be favorited by the same user twice.
        unique_together = (('user'),('movie'))
        # Similarly, for indexing purposes, we will only accept
        # values that follow the previous rule.
        index_together = (('user'),('movie'))