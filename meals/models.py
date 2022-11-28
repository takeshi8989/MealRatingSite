from django.db import models
import datetime


class Tag(models.Model):
    tagName = models.CharField(max_length=30)

    def __str__(self):
        return self.tagName


class Meal(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    imgUrl = models.TextField()
    countryOfOrigin = models.CharField(max_length=30)
    dateAdded = models.DateField(default=datetime.date.today)
    avgRating = models.FloatField(default=0)
    numOfVotes = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'meals'

        
class MealRating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    rating = models.FloatField()
    reviewer =models.ForeignKey('user.User', on_delete=models.CASCADE, blank=True, null=True)
    dateOfRating = models.DateField(default=datetime.date.today)

    class Meta:
        db_table = 'ratings'