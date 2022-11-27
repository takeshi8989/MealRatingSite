from django.shortcuts import render
from .models import Meal, MealRating, Tag
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, NewMealForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def home(request):
    morningMeals = Tag.objects.get(tagName='Morning').meal_set.all()[0:3]
    afternoonMeals = Tag.objects.get(tagName='Afternoon').meal_set.all()[0:3]
    eveningMeals = Tag.objects.get(tagName='Evening').meal_set.all()[0:3]
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


def category(request, tags, sortBy):
    tagList = ['Vegetarian', 'Spicy', 'Healthy', 'Seafood', 'Morning', 'Afternoon', 'Evening']
    selectedTags = tags.split('+')
    mealList = Meal.objects.none()
    for i in range(0, len(selectedTags)):
        if not selectedTags[i].__eq__('Recommended'):
            if selectedTags[i] in tagList:
                mealList = mealList | Tag.objects.get(tagName=selectedTags[i]).meal_set.all()
    mealList = mealList.distinct()
    if sortBy == 'date':
        mealList = mealList.order_by('-dateAdded')
    if sortBy == 'rating':
        mealList = mealList.order_by('-avgRating')
    if sortBy == 'country':
        mealList = mealList.order_by('countryOfOrigin')
    categoryCxt = {
        'mealList': mealList,
        'sortBy': sortBy,
        'tags': tags,
        'tagList': tagList
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

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home', tags='+Vegetarian+RecommendedSpicy+Healthy+Seafood+', sortBy='date')
    else:
        form = SignUpForm()
    return render(request, 'meals/register.html', context={'form': form})

@login_required(login_url='/register')
def addMeal(request):
    if request.method == 'POST':
        form = NewMealForm(request.POST)
        if form.is_valid():
            mealName = form.cleaned_data['name']
            mealUrl = form.cleaned_data['imgUrl']
            mealOrigin = form.cleaned_data['countryOfOrigin']
            mealDescription = form.cleaned_data['description']
            meal = Meal(name=mealName, description=mealDescription ,imgUrl=mealUrl, countryOfOrigin=mealOrigin)
            meal.save()
            tags = form.cleaned_data['tags']
            for tag in tags:
                meal.tags.add(tag)
            meal.save()

        return redirect('home', tags='+Vegetarian+RecommendedSpicy+Healthy+Seafood+', sortBy='date')
    else:
        form = NewMealForm()
    return render(request, 'meals/addMeal.html', context={'form': form})

@login_required(login_url='/register')
def history(request):
    return render(request, 'meals/history.html')