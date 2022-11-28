from faker import Faker
from .models import Meal

fake = Faker()

for i in range(2):
    name = fake.name()
    firstName = name.split(" ")[0]
    lastName = name.split(" ")[len(name.split(" ")) - 1]
    username = firstName
    email = fake.email()
    password = fake.password()

    # user = User(username=username, last_name=lastName, first_name=firstName, password=password)
    print(Meal.objects.all())
    # user.save()

# def generateNewUser():
# ...     person = User.objects.create_user(username=fake.name(), email=fake.email(), password=fake.password()) 
# ...     for i in range(10):
# ...             currentId = fake.random_int(1, 28)
# ...             if Meal.objects.filter(id=currentId).exists():
# ...                     meal = Meal.objects.get(id=currentId)
# ...                     rating = MealRating(meal=meal, rating=fake.random_int(1,5))
# ...                     rating.save()
# ...                     meal.avgRating = (meal.avgRating * meal.numOfVotes + rating.rating) / (meal.numOfVotes + 1)
# ...                     meal.numOfVotes += 1
# ...                     person.ratings.add(rating)
# ...                     meal.save()