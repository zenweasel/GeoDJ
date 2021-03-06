from django.db import models
from django.utils.encoding import smart_str
from geodj.youtube import YoutubeMusic

class Country(models.Model):
    name = models.TextField()
    iso_code = models.CharField(max_length=2, unique=True)
    continent = models.TextField()

    def __unicode__(self):
        return self.name

    def random_artists(self):
        return self.artist_set.all().order_by('?')

    @staticmethod
    def with_artists(min=1):
        return Country.objects.annotate(number_of_artists=models.Count('artist')).filter(number_of_artists__gte=min)

class Genre(models.Model):
    name = models.TextField(unique=True)

    def __unicode__(self):
        return self.name

class Artist(models.Model):
    name = models.TextField()
    mbid = models.TextField(unique=True)
    country = models.ForeignKey(Country)
    genres = models.ManyToManyField(Genre)

    def __unicode__(self):
        return self.name

    def youtube_videos(self):
        return YoutubeMusic().search(smart_str(self.name))

    @staticmethod
    def by_genre(genre_name):
        return Artist.objects.filter(genres__name=genre_name)
