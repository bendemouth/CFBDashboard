from django.db import models
from django.utils.text import slugify


# Create your models here.
class Team(models.Model):
    api_id = models.IntegerField(unique=True)
    school = models.CharField(max_length=100)
    abbr = models.CharField(max_length=10)
    conference = models.CharField(max_length=100)
    division = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.school

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.school)
        super().save(*args, **kwargs)




class TeamStat(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='stats',
        related_query_name='stat'
    )
    conference = models.CharField(max_length=100)
    stat = models.CharField(max_length=100)
    stat_value = models.IntegerField()

    def __str__(self):
        return f"{self.school} - {self.stat}"