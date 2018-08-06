from django.contrib import admin
from django.db.models import Avg

from .models import *
from .admin_filters import PopularityFilter


@admin.register(MealCategory)
class MealCategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'image_url')
    list_display = ['name', 'meals_amount']

    def meals_amount(self, obj):
        amount = Meal.objects.filter(category=obj).count()
        return amount if amount > 0 else "None"


    meals_amount.empty_value_display = "None"


@admin.register(Meal)
class MealAdminAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'recipes_amount')
    list_filter = ['category', PopularityFilter]
    change_list_template = 'admin/meal/meal_change_list.html'

    def recipes_amount(self, obj):
        amount = obj.recipes_amount

        return amount if amount > 0 else "None"


@admin.register(MealRecipe)
class MealRecipeAdmin(admin.ModelAdmin):
    list_display = ['name_info', 'meal_name', 'meal_category']
    list_filter = ['meal__category']
    search_fields = ['author__username', 'author__email']
    readonly_fields = ['author', 'comments_stats']
    filter_horizontal = ['ingredients', 'measures']
    fields = ('name', 'author', 'instructions', 'ingredients',
              'measures', 'comments_stats', 'tags',
              'area', 'image_url', 'movie_url')

    def name_info(self, obj):
        return "{0} by: {1}".format(obj.name, obj.author.username.title())

    def meal_name(self, obj):
        return obj.meal.name

    def meal_category(self, obj):
        return obj.meal.category.name

    def comments_stats(self, obj):
        comments = obj.comments.all()
        if comments.count() > 0:
            return "{0} Comments, Average rate: {1}".format(comments.count(), comments.aggregate(Avg('rating')).get('rating__avg'))
        else:
            return "Not commented yet"


@admin.register(RecipeComment)
class RecipeCommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'target', 'rating']
    list_filter = ['rating']
    search_fields = ['author__username', 'author__email']
    readonly_fields = ['author']

    def target(self, obj):
        return "{0} by {1}".format(obj.target, obj.target.author.email)

    def name(self, obj):
        return str(obj)
