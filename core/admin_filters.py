from django.contrib import admin
from django.db.models import Q, Avg, Count

from .models import Meal, MealRecipe


class PopularityFilter(admin.SimpleListFilter):
    title = ('popularity')
    parameter_name = 'recipes_amount'

    def lookups(self, request, model_admin):
        return (
            ('0', ('Not popular')),
            ('1', ('Normal')),
            ('2', ('Very Popular'))
        )

    def queryset(self, request, queryset):
        qs = queryset.annotate(num_recipes=Count('mealrecipe_recipes'))
        avg = qs.filter(num_recipes__gt=0).aggregate(Avg('num_recipes')).get('num_recipes__avg') + 1
        avg = 4.5 if avg >= 4.5 else avg
        if self.value() == '0':
            return qs.filter(num_recipes=0)

        if self.value() == '1':
            return qs.filter(num_recipes__gt=0)

        if self.value() == '2':
            return qs.filter(num_recipes__gt=avg)
