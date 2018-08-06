from django.test import TestCase

from core.models import *
from testing_data import *

class ModelTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(ModelTests, cls).setUpClass()
        user, created = User.objects.get_or_create(username=SUPERUSER_DATA.get('username'),
                                                  email=SUPERUSER_DATA.get('email'),
                                                  is_superuser=1,
                                                  is_staff=1)
        if created:
            user.set_password(SUPERUSER_DATA.get(('password')))
            user.save()

        meal_category, cat_created = MealCategory.objects.get_or_create(**MEAL_CATEGORY_DATA)

        meal, meal_created = Meal.objects.get_or_create(category=meal_category, **MEAL_DATA)

        meal_recipe, recipe_created = MealRecipe.objects.get_or_create(author=user, meal=meal, **MEAL_RECIPE_DATA)

        comment, comment_created = RecipeComment.objects.get_or_create(author=user, **COMMENT_DATA)
        meal_recipe.comments.add(comment)

        area, area_created = MealArea.objects.get_or_create(**AREA_DATA)

        tag, tag_created = MealTag.objects.get_or_create(**TAG_DATA)
        ingredient, ingredient_created = MealIngredient.objects.get_or_create(name=INGREDIENT_DATA.get('name'))
        measure, measure_created = MealIngredientMeasure.objects.get_or_create(quantity=INGREDIENT_DATA.get('quantity'))

    def test_user_setUp(self):
        user = User.objects.first()
        self.assertIsInstance(user, User, "created user is not an instance of auth.User")

    def test_meal_category_setUp(self):
        category = MealCategory.objects.first()
        self.assertIsInstance(category, MealCategory)
        self.assertEqual(category.name, MEAL_CATEGORY_DATA.get('name'))
        self.assertEqual(category.description, MEAL_CATEGORY_DATA.get('description'))

    def test_meal_setUp(self):
        meal = Meal.objects.first()
        self.assertIsInstance(meal, Meal)
        self.assertEqual(meal.name, MEAL_DATA.get('name'))

    def test_meal_recipe_setUp(self):
        recipe = MealRecipe.objects.first()
        self.assertIsInstance(recipe, MealRecipe)
        self.assertEqual(recipe.name, MEAL_RECIPE_DATA.get('name'))
        self.assertEqual(recipe.author, User.objects.first())
        self.assertEqual(recipe.meal, Meal.objects.first())

    def test_meal_test_object(self):
        meal = Meal.get_test_object(MealCategory.objects.first())
        self.assertIsInstance(meal, Meal, "Meal test object is not an instance of Meal")

    def test_meal_recipe_test_object(self):
        recipe = MealRecipe.get_test_object(User.objects.first(), Meal.objects.first())
        self.assertIsInstance(recipe, MealRecipe, "MealRecipe test object is not an instance of MealRecipe")

    def test_recipe_comment_target(self):
        target = RecipeComment.objects.first().target
        self.assertIsInstance(target, MealRecipe)

    def test_recipe_comment_str(self):
        comment = RecipeComment.objects.first()
        self.assertEqual(str(comment), "Comment by: "+SUPERUSER_DATA.get('email'))

    def test_meal_area_str(self):
        area = MealArea.objects.first()
        self.assertEqual(str(area), AREA_DATA.get('name'))

    def test_meal_tag_str(self):
        tag = MealTag.objects.first()
        self.assertEqual(str(tag), TAG_DATA.get('label'))

    def test_ingredient_str(self):
        ing = MealIngredient.objects.first()
        self.assertEqual(str(ing), INGREDIENT_DATA.get('name'))

    def test_measure_str(self):
        measure = MealIngredientMeasure.objects.first()
        self.assertEqual(str(measure), INGREDIENT_DATA.get('quantity'))

    def test_category_str(self):
        category = MealCategory.objects.first()
        self.assertEqual(str(category), MEAL_CATEGORY_DATA.get('name'))

    def test_meal_str(self):
        meal = Meal.objects.first()
        self.assertEqual(str(meal), MEAL_DATA.get('name'))

    def test_meal_recipes_amount(self):
        meal = Meal.objects.first()
        self.assertEqual(meal.recipes_amount, 1)

    def test_recipes_str(self):
        recipe = MealRecipe.objects.first()
        self.assertEqual(str(recipe), MEAL_RECIPE_DATA.get('name'))

    def test_recipes_owner(self):
        recipe = MealRecipe.objects.first()
        self.assertEqual(recipe.owner, User.objects.first())