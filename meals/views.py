from django.shortcuts import render
from .models import Meal, MealRating, Tag
from user.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, NewMealForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def home(request):
    if request.method == 'POST':
        name = request.POST['username']
        pw = request.POST['password']
        user = authenticate(username=name, password=pw)
        if user:
            login(request,user)
            return redirect('home', tags='+Vegetarian+Spicy+Healthy+Seafood+Morning+Afternoon+Evening+Recommended+', sortBy='date')
    return render(request, 'meals/landing.html')


def category(request, tags, sortBy):
    tagList = ['Vegetarian', 'Spicy', 'Healthy', 'Seafood', 'Morning', 'Afternoon', 'Evening']
    selectedTags = tags.split('+')
    mealList = Meal.objects.none()
    for i in range(0, len(selectedTags)):
        if not selectedTags[i].__eq__('Recommended'):
            if selectedTags[i] in tagList:
                mealList = mealList | Tag.objects.get(tagName=selectedTags[i]).meal_set.all()
    user = request.user
    if 'Recommended' in tags and user.is_authenticated:
        favorite = user.ratings.filter(rating__gte=4).order_by('?').first()
        if favorite is not None:
            theMeal = favorite.meal
            similarUser = MealRating.objects.filter(meal=favorite.meal).filter(reviewer__isnull=False).exclude(reviewer=user).order_by('?').first().reviewer
            recommend = similarUser.ratings.filter(rating__gte=4).exclude(meal=theMeal)
            for re in recommend:
                mealList = mealList | Meal.objects.filter(id=re.meal.id)

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
            return redirect('home', tags='+Vegetarian+Spicy+Healthy+Seafood+Morning+Afternoon+Evening+Recommended+', sortBy='date')
    return render(request, 'meals/category.html', context=categoryCxt)


def detail(request, mealId):
    meal = Meal.objects.filter(id=mealId).first()
    if meal is None:
        return render(request, 'meals/notfound.html')
    if request.method == 'POST' and 'ratingBtn' in request.POST:
        newRate = int(request.POST['rating'])
        newRating = MealRating(meal=meal, rating=newRate)
        meal.avgRating = (meal.avgRating * meal.numOfVotes + newRate) / (meal.numOfVotes + 1)
        meal.numOfVotes += 1
        meal.save()
        newRating.save()
        user = request.user
        if user.is_authenticated:
            user.ratings.add(newRating)
            newRating.reviewer = user
        return redirect('home', tags='+Vegetarian+Spicy+Healthy+Seafood+Morning+Afternoon+Evening+Recommended+', sortBy='date')
    elif request.method == 'POST' and 'loginBtn' in request.POST:
        name = request.POST['username']
        pw = request.POST['password']
        user = authenticate(username=name, password=pw)
        if user:
            login(request,user)
            return redirect('home', tags='+Vegetarian+Spicy+Healthy+Seafood+Morning+Afternoon+Evening+Recommended+', sortBy='date')
    return render(request, 'meals/detail.html', context={'meal': meal})

def log_out(request):
    logout(request)
    return render(request, 'meals/logout.html')

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home', tags='+Vegetarian+Spicy+Healthy+Seafood+Morning+Afternoon+Evening+Recommended+', sortBy='date')
    else:
        form = SignUpForm()
    return render(request, 'meals/register.html', context={'form': form})

@login_required(login_url='/register')
def addMeal(request):
    if request.method == 'POST':
        form = NewMealForm(request.POST)
        if form.is_valid():
            user = request.user
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
            user = request.user
            user.meals.add(meal)

        return redirect('home', tags='+Vegetarian+Spicy+Healthy+Seafood+Morning+Afternoon+Evening+Recommended+', sortBy='date')
    else:
        form = NewMealForm()
    return render(request, 'meals/addMeal.html', context={'form': form})

@login_required(login_url='/register')
def history(request):
    user = request.user
    meals = user.meals.all().order_by('-dateAdded')
    ratings = user.ratings.all().order_by('-dateOfRating')
    return render(request, 'meals/history.html', context={'meals': meals, 'ratings': ratings})