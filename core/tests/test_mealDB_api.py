from django.test import TestCase
from ..api_handler import *

import requests


class MealDBTestCase(TestCase):
    def test_api_key(self):
        key = API_KEY.get_api_key()
        self.assertEqual(key, 1)
        str_key = API_KEY.to_string()
        self.assertEqual(str_key, str(key))

    def test_api_url_categories(self):
        categories_url = API_URL.get_categories()
        result = dict(requests.get(url=categories_url).json())
        self.assertIn('categories', result.keys())

    def test_api_url_meals(self):
        meals_url = API_URL.get_meals_by_category(category_name='Beef')
        result = dict(requests.get(url=meals_url).json())
        self.assertIn('meals', result.keys())
        self.assertIn('idMeal', result.get('meals')[0])

    def test_api_url_recipes(self):
        meals_url = API_URL.get_meals_by_category(category_name='Beef')
        meal_result = dict(requests.get(url=meals_url).json())
        mealID = meal_result.get('meals')[0]

        recipes_url = API_URL.get_meal_details_by_id(meal_id=mealID.get('idMeal'))
        recipes_result = dict(requests.get(url=recipes_url).json())
        self.assertIn('meals', recipes_result.keys())
        test_recipe = dict(recipes_result.get('meals')[0])
        self.assertIn('idMeal', test_recipe.keys())
        self.assertIn('strMeal', test_recipe.keys())
        self.assertIn('strCategory', test_recipe.keys())
        self.assertIn('strArea', test_recipe.keys())
        self.assertIn('strInstructions', test_recipe.keys())
