from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

from rest_framework.reverse import reverse as api_reverse


class RecipeComment(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    content = models.CharField(max_length=2000, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=3)

    class Meta:
        verbose_name_plural='Recipe Comments'

    @property
    def target(self):
        return self.mealrecipe_target.first()

    def __str__(self):
        return "Comment by: " + self.author.email


class MealArea(models.Model):
    name = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.name


class MealTag(models.Model):
    label = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.label


class MealIngredient(models.Model):
    name = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.name


class MealIngredientMeasure(models.Model):
    quantity = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.quantity


class MealCategory(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=500, blank=False)
    image_url = models.URLField()

    class Meta:
        verbose_name_plural = 'Meal Categories'

    def __str__(self):
        return self.name

    def get_api_url(self, request=None):
        return api_reverse("api:category-rud", kwargs={'name': self.name}, request=request)


class Meal(models.Model):
    name = models.URLField(max_length=100, blank=False)
    description = models.URLField(max_length=500, blank=True)
    category = models.ForeignKey(to=MealCategory, on_delete=models.CASCADE, blank=False)
    image_url = models.URLField()

    def __str__(self):
        return self.name

    def get_api_url(self, request=None):
        return api_reverse("api:meal-recipes-rud", kwargs={'pk': self.pk}, request=request)

    @property
    def recipes(self):
        return self.mealrecipe_recipes.all()

    @property
    def recipes_amount(self):
        return self.mealrecipe_recipes.count()

    @classmethod
    def get_test_object(cls, category):
        obj, created = Meal.objects.get_or_create(name='test_meal',
                                                        description="Test DESC",
                                                        category=category,
                                                        image_url="Http://image.com/image.png")
        return obj


class MealRecipe(models.Model):
    name = models.CharField(max_length=200, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    instructions = models.CharField(max_length=2000, blank=False)
    ingredients = models.ManyToManyField(to=MealIngredient)
    measures = models.ManyToManyField(to=MealIngredientMeasure)
    comments = models.ManyToManyField(to=RecipeComment, related_name="%(class)s_target")
    tags = models.ManyToManyField(to=MealTag)
    area = models.ForeignKey(to=MealArea, on_delete=models.CASCADE, null=True)
    meal = models.ForeignKey(to=Meal, related_name="%(class)s_recipes",
                             on_delete=models.CASCADE, null=False)
    image_url = models.URLField(blank=True)
    movie_url = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = 'Meal Recipes'

    @classmethod
    def get_test_object(cls, author, meal):
        obj, created = MealRecipe.objects.get_or_create(name="Test_MealRecipe",
                                                        instructions="Bla bla bla",
                                                        author=author,
                                                        meal=meal)
        return obj

    def __str__(self):
        return self.name

    @property
    def owner(self):
        return self.author

    def get_api_url(self, request=None):
        return api_reverse("api:recipe-details", kwargs={'pk': self.pk}, request=request)



