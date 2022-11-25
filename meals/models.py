from django.db import models
import datetime

# Create your models here.
class Meal(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    imgUrl = models.TextField()
    countryOfOrigin = models.CharField(max_length=30)
    typicalMealTime = models.IntegerField(default=0)
    dateAdded = models.DateField(default=datetime.date.today)
    avgRating = models.FloatField(default=0)
    numOfVotes = models.IntegerField(default=0)

    class Meta:
        db_table = 'meals'

class MealRating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    rating = models.FloatField()
    dateOfRating = models.DateField(default=datetime.date.today)

    class Meta:
        db_table = 'ratings'