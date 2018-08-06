from django.urls import path

from .views import RegisterAPIView, MealCategoriesRudView, MealCategoryAPIView, MealRecipeListAPIView, MealByCategoryListAPIView, MealRecipeDetailsAPIView

app_name = 'api'
urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('categories/', MealCategoryAPIView.as_view(), name='categories'),
    path('categories/<str:name>', MealCategoriesRudView.as_view(), name='category-rud'),
    path('categories/<str:name>/meals/', MealByCategoryListAPIView.as_view(), name='category-meals'),
    path('meal/<int:pk>/recipes/', MealRecipeListAPIView.as_view(), name='meal-recipes-rud'),
    path('recipe/<int:pk>/details', MealRecipeDetailsAPIView.as_view(), name='recipe-details'),
]
