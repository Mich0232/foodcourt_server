from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError
from django.db.models import Avg, Q
from django.contrib.auth.models import User

from core.models import MealCategory, Meal, MealRecipe
from .forms import UserRegistrationForm


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=250, required=True)
    email = serializers.EmailField(max_length=250, required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(style={'input_type': 'password'},
                                     max_length=250,
                                     required=True)

    def create(self, validated_data):
        new_user = User.objects.create(username=validated_data.get('username'),
                                       email=validated_data.get('email'))
        new_user.set_password(validated_data.get('password'))
        new_user.save()
        return new_user

    def update(self, instance, validated_data):
        return instance


class MealCategorySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MealCategory
        fields = [
            'url',
            'name',
            'description',
            'image_url'
        ]
        read_only_fields = ['url']

    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)


class MealSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Meal
        fields = [
            'url',
            'name',
            'description',
            'image_url'
        ]
        read_only_fields = ['url', 'name']

    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)


class MealRecipeListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    author = serializers.SerializerMethodField(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MealRecipe
        fields = [
            'url',
            'author',
            'image_url',
            'rating'
        ]

    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)

    def get_rating(self, obj):
        comments = obj.comments.all()
        rating = comments.aggregate(Avg('rating')).get('rating__avg') if comments.count() > 0 else "No comments yet"
        return str(rating)

    def get_author(self, obj):
        return obj.author.username if obj.author.username else obj.author.emai


class MealRecipeSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)
    ingredients = serializers.SerializerMethodField()
    measures = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = MealRecipe
        fields = [
            'name',
            'author',
            'instructions',
            'ingredients',
            'measures',
            'comments',
            'tags',
            'area',
            'image_url',
            'movie_url'
        ]

    def get_ingredients(self, obj):
        return [ing.name for ing in obj.ingredients.all()]

    def get_measures(self, obj):
        return [measure.quantity for measure in obj.measures.all()]

    def get_area(self, obj):
        return obj.area.name

    def get_tags(self, obj):
        return [tag.label for tag in obj.tags.all()]

    def get_author(self, obj):
        return obj.author.username if obj.author.username else obj.author.email
