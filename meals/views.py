from django.shortcuts import render
from .models import Meal, MealRating
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def home(request):
    morningMeals = Meal.objects.filter(typicalMealTime=1)[0:3]
    afternoonMeals = Meal.objects.filter(typicalMealTime=2)[0:3]
    eveningMeals = Meal.objects.filter(typicalMealTime=3)[0:3]
    recentMeals = Meal.objects.all().order_by('-dateAdded')[0:3]
    topRatedMeals = Meal.objects.all().order_by('-avgRating')[0:3]
    ctx = {
        'morning': morningMeals,
        'afternoon': afternoonMeals,
        'evening': eveningMeals,
        'recent': recentMeals,
        'topRated': topRatedMeals
    }
    if request.method == 'POST':
        mealName = request.POST['name']
        mealUrl = request.POST['url']
        mealOrigin = request.POST['origin']
        mealTime = int(request.POST['time'])
        mealDescription = request.POST['description']
        meal = Meal(name=mealName, description=mealDescription ,imgUrl=mealUrl, countryOfOrigin=mealOrigin, typicalMealTime=mealTime)
        meal.save()
    return render(request, 'meals/index.html', context=ctx)


def category(request):
    mealList = Meal.objects.all()
    categoryCxt = {
        'mealList': mealList,
    }
    if request.method == 'POST':
        name = request.POST['username']
        pw = request.POST['password']
        user = authenticate(username=name, password=pw)
        if user:
            login(request,user)
    return render(request, 'meals/category.html', context=categoryCxt)


def detail(request, mealId):
    meal = Meal.objects.filter(id=mealId).first()
    if meal is None:
        return render(request, 'meals/notfound.html')
    if request.method == 'POST':
        newRate = int(request.POST['rating'])
        newRating = MealRating(meal=meal, rating=newRate)
        meal.avgRating = (meal.avgRating * meal.numOfVotes + newRate) / (meal.numOfVotes + 1)
        meal.numOfVotes += 1
        meal.save()
        newRating.save()
    return render(request, 'meals/detail.html', context={'meal': meal})

def log_out(request):
    logout(request)
    return render(request, 'meals/logout.html')