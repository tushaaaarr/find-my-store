from email.policy import default
from django.db import models
from django.contrib.auth.models import User 
import jsonfield
from datetime import datetime

class user_type(models.Model):
    is_user = models.BooleanField(default=False)
    is_merchant  = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.is_merchant == True:
            return str(self.user) + str(' ') + " - is_merchant"
        elif self.is_user == True:
            return str(self.user) + str(' ') + " - is_user"


class Store(models.Model):
    store_name = models.CharField(max_length=20)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    def __str__(self):
        return self.store_name


CATEGORY_CHOICES =(
    ("1", "Vegetarian"),
    ("2", "Non-Vegetarian"),
)

class Recipe(models.Model):
    # user = models.ForeignKey(Store,on_delete=models.CASCADE)
    food_name = models.CharField(max_length=100)
    category = models.CharField(max_length=5,choices=CATEGORY_CHOICES)
    desc = models.TextField(default='' )
    ingredients = jsonfield.JSONField()
    pub_date=models.DateField(default=datetime.now())
    price = models.PositiveIntegerField(default=0)
    image = models.FileField(upload_to = 'media')
    def __str__(self):
        return str(self.food_name)


class RecipeImage(models.Model):
    recipe = models.ForeignKey(Recipe, default=None, on_delete=models.CASCADE)
    images = models.FileField(upload_to = 'media')
    def __str__(self):
        return self.recipe.food_name

class DiscountSym(models.Model):
    user = models.OneToOneField(Store,on_delete=models.CASCADE)
    ingredients_discount = jsonfield.JSONField()
    def __str__(self):
        return str(self.user.store_name)


