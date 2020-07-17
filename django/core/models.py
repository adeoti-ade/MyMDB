from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Sum

from uuid import uuid4


class MovieManager(models.Manager):
    def all_with_related_persons(self):
        qs = self.get_queryset()
        qs = qs.select_related('director')
        qs = qs.prefetch_related('writers', 'actors')

        return qs

    def all_with_related_persons_and_score(self):
        qs = self.all_with_related_persons()
        qs = qs.annotate(score=Sum("vote__value"))
        return qs
        
    

class Movie(models.Model):
    NOT_RATED = 0
    RATED_G = 1
    RATED_PG = 2
    RATED_R = 3
    RATINGS = (
        (NOT_RATED, 'NR - NOT Rated'),
        (RATED_G, 'G - General Audience'),
        (RATED_PG, 'PG - Parental Guidance'),
        (RATED_R, 'R - Restricted')
    )

    title = models.CharField(max_length=140)
    plot = models.TextField()
    year = models.PositiveIntegerField()
    rating = models.IntegerField(choices=RATINGS, default=NOT_RATED)
    runtime = models.PositiveIntegerField()
    website = models.URLField(blank=True)
    director = models.ForeignKey(to='Person',
                                on_delete=models.SET_NULL,
                                related_name='directed',
                                null=True,
                                blank=True)
    writers = models.ManyToManyField(to='Person',
                                     related_name='writing_credits',
                                     blank=True)
    actors = models.ManyToManyField(to='Person',
                                    through='Role',
                                    related_name='acting_credits',
                                    blank=True)

    objects = MovieManager()
    

    class Meta:
        ordering = ('-year', 'title')


    def __str__(self):
        return "{} ({})".format(self.title, self.year)

class PersonManager(models.Manager):

    def all_with_prefetch_movies(self):
        qs = self.get_queryset()

        return qs.prefetch_related(
            'directed',
            'writing_credits',
            'role_set__movie'
        )
    
class Person(models.Model):
    last_name = models.CharField(max_length=140)
    first_name = models.CharField(max_length=140)
    born = models.DateField()
    died = models.DateField(null=True, blank=True)

    objects = PersonManager()

    class Meta:

        ordering = ('last_name', 'first_name')

    def __str__(self):
        if self.died:
            return "{}, {} ({} - {})".format(
                self.first_name,
                self.last_name,
                self.born,
                self.died
            )
        return "{}, {} ({})".format(
            self.first_name,
            self.last_name,
            self.born
        )

class Role(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING)
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=140)

    def __str__(self):

        return "{} {} {}".format(self.movie, self.person, self.name)

    class Meta:

        unique_together = ('movie',
                            'person',
                            'name')

class VoteManager(models.Manager):
    def get_vote_or_unsaved_blank_vote(self, movie, user):
        try:
            return Vote.objects.get(movie=movie, user=user)
        except ObjectDoesNotExist:
            return Vote(movie=movie, user=user)

class Vote(models.Model):

    UP = 1
    DOWN = -1
    VALUE_CHOICES = (
            (UP, "Like"),
            (DOWN, "Dislike"))
    value = models.SmallIntegerField(choices=VALUE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    voted_on = models.DateTimeField(auto_now=True)

    objects = VoteManager()

    class Meta:
        unique_together = ('user', 'movie')


def movie_directory_path_with_uuid(instance, filename):
    return "{}/{}".format(instance, filename)

class MovieImage(models.Model):
    image = models.ImageField(upload_to=movie_directory_path_with_uuid)
    uploaded = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
