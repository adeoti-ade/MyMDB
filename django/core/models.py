from django.db import models

# Create your models here.

class Movie(models.Model):
    NOT_RATED = 0
    RATED_G = 1
    RATED_PG = 2
    RATED_R = 3
    RATINGS = (
        (NOT_RATED, 'NR - NOT Rated),
        (RATED_G, 'G - General Audience'),
        (RATED_PG, 'PG - Parental Guidance'),
        (RATED_R, 'R - Restricted')
    )

    title = models.CharField(max_length=140)
    plot = models.TextField()
    year = models.PositiveIntegerField()
    rating = models.IntegerField(choices=RATINGS, default=NOT_RATED)
    runtime = models.PositiveIntegerField()
    website = models.UrlField(blank=True)

    def __str__(self):
        return "{} ({})".format(self.title, self.year)