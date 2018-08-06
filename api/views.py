from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

from .serializers import UserRegisterSerializer, MealCategorySerializer, MealSerializer, MealRecipeSerializer, MealRecipeListSerializer
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly, IsNotAuthenticated
from core.models import MealCategory, MealRecipe, Meal


class MealCategoryAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    """ Meal Categories List View """
    lookup_field = 'name'
    serializer_class = MealCategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return MealCategory.objects.all()

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MealCategoriesRudView(generics.RetrieveUpdateDestroyAPIView):
    """ Meal Categories Rud View """
    lookup_field = 'name'
    serializer_class = MealCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return MealCategory.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class MealByCategoryListAPIView(generics.ListAPIView):
    """ Meals by category List View """
    lookup_field = 'name'
    serializer_class = MealSerializer
    permission_classes = []

    def get_queryset(self):
        return Meal.objects.filter(category__name=self.kwargs['name'])

    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}


# TODO: create model should be in another view???
class MealRecipeListAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    """ Meal Recipes List View"""
    lookup_field = 'pk'
    serializer_class = MealRecipeListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Meal.objects.get(pk=self.kwargs.get('pk')).recipes

    def post(self, request, *args, **kwargs):
        """ Create new recipe"""
        pass


class MealRecipeDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ Meal Recipe Details Rud View """
    lookup_field = 'pk'
    serializer_class = MealRecipeSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        return MealRecipe.objects.get(pk=self.kwargs.get('pk'))

    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}


class RegisterAPIView(generics.CreateAPIView):
    permission_classes = [IsNotAuthenticated]
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



