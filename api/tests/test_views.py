from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from django.urls import reverse as dj_reverse
from rest_framework.test import APIClient

import requests, os, json

from testing_data import USER_DATA as USER_LOGIN_DATA, SUPERUSER_DATA as SUPERUSER_LOGIN_DATA
from testing_data import *
from core.models import MealCategory, MealRecipe,\
    Meal, MealArea, MealTag, MealIngredientMeasure, MealIngredient

from ..serializers import *


def get_login_data(username, password):
    return dict({'username': username, 'password': password})


client = APIClient()


class DataBaseInitTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(DataBaseInitTest, cls).setUpClass()
        superuser, created = User.objects.get_or_create(username=SUPERUSER_LOGIN_DATA['username'],
                                                        email=SUPERUSER_LOGIN_DATA['email'],
                                                        is_superuser=1,
                                                        is_staff=1)
        if created:
            superuser.set_password(SUPERUSER_LOGIN_DATA['password'])
            superuser.save()

        user, user_created = User.objects.get_or_create(username=USER_LOGIN_DATA['username'], email=USER_LOGIN_DATA['email'])
        if user_created:
            user.set_password(USER_LOGIN_DATA['password'])
            user.save()

        category, category_created = MealCategory.objects.get_or_create(**MEAL_CATEGORY_DATA)

        meal, meal_created = Meal.objects.get_or_create(category=category, **MEAL_DATA)
        recipe, recipe_created = MealRecipe.objects.get_or_create(author=superuser, meal=meal, **MEAL_RECIPE_DATA)
        ingredient, ing_created = MealIngredient.objects.get_or_create(name=INGREDIENT_DATA.get('name'))

        measure, measure_created = MealIngredientMeasure.objects.get_or_create(quantity=INGREDIENT_DATA.get('quantity'))

        area, area_created = MealArea.objects.get_or_create(**AREA_DATA)
        tag, tag_created = MealTag.objects.get_or_create(**TAG_DATA)

        recipe.ingredients.add(ingredient)
        recipe.measures.add(measure)
        recipe.tags.add(tag)
        recipe.area = area
        recipe.save()


    def test_user(self):
        user = User.objects.filter(is_superuser=0).first()
        self.assertEqual(user.username, USER_LOGIN_DATA['username'])
        self.assertEqual(user.email, USER_LOGIN_DATA['email'])
        self.assertNotEquals(user.is_superuser, 1)

    def test_superuser(self):
        user = User.objects.filter(is_superuser=1).first()
        self.assertEqual(user.username, SUPERUSER_LOGIN_DATA['username'])
        self.assertEqual(user.email, SUPERUSER_LOGIN_DATA['email'])
        self.assertNotEquals(user.is_superuser, 0)

    def test_meal_cat(self):
        meal_categories = MealCategory.objects.all()
        self.assertEqual(len(meal_categories), 1)

    def test_api_login_with_email(self):
        data = get_login_data(USER_LOGIN_DATA['email'], USER_LOGIN_DATA['password'])
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_api_login_with_username(self):
        data = get_login_data(USER_LOGIN_DATA['username'], USER_LOGIN_DATA['password'])
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_create_meal_category_by_user(self):
        data = get_login_data(USER_LOGIN_DATA['email'], USER_LOGIN_DATA['password'])
        login_url = api_reverse("api-login")
        client = APIClient()
        response = client.post(login_url, data, format='json')
        if response.status_code == status.HTTP_200_OK:
            self.access_token = response.data.get('access')
            data = {'name': "TestName", 'description': "Test Description", 'image_url': "http://image.com/image.jpg"}
            url = BASE_URL + dj_reverse("api:categories")
            head = {'Authorization': 'Bearer ' + str(self.access_token)}
            response = requests.post(url, data, headers=head)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        else:
            self.fail("Unable to login")
        client.logout()

    def test_create_meal_category_by_superuser(self):
        data = get_login_data(SUPERUSER_LOGIN_DATA['email'], SUPERUSER_LOGIN_DATA['password'])
        login_url = api_reverse("api-login")
        client = APIClient()
        response = client.post(login_url, data, format='json')
        if response.status_code == status.HTTP_200_OK:
            self.access_token = response.data.get('access')
            data = {'name': "TestName", 'description': "Test Description", 'image_url': "http://image.com/image.jpg"}
            url = BASE_URL + dj_reverse("api:categories")
            head = {'Authorization': 'Bearer ' + str(self.access_token)}
            response = requests.post(url, data, headers=head)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        else:
            self.fail("Unable to login")
        client.logout()

    def test_get_item(self):
        meal_category = MealCategory.objects.first()
        url = meal_category.get_api_url()
        response = self.client.get(url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #  TODO: 'access' property test

    def test_post_item_not_user(self):
        self.client.logout()
        data = {'name': "TestName", 'description': "Test Description", 'image_url': "http://image.com/image.jpg"}
        url = api_reverse("api:categories")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    #     TODO: API categories list test
    def test_api_categories_list(self):
        response = self.client.get(api_reverse('api:categories'), data={}, format='json')
        category = MealCategory.objects.filter(name=MEAL_CATEGORY_DATA.get('name'))
        serialized_category = MealCategorySerializer(category)
        category_from_api = response.json()[0]
#

    def test_register_user_api(self):
        response = self.client.post(api_reverse('api:register'), data=SUPERUSER_LOGIN_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reqister_create_new(self):
        response = self.client.post(api_reverse('api:register'),
                                    data={'username': 'tester2',
                                          'email': 'tester2@mail.pl',
                                          'password': 'test1234'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)