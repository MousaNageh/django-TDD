import imp
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from recipe.serializers import RecipeSerializer
from core.models import Recipe

RECIPE_URL = reverse("recipe:recipe-list")

def sample_recipe(user,**params):
    default = {
        'title':'sample recipe',
        'time_minutes':10,
        'price':15.00
    }
    default.update(params)
    return Recipe.objects.create(user=user,**default)

class PublicRecipeApiTests(TestCase):
    def setUp(self) :
        self.client = APIClient()

    def test_auth_is_required(self):
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)

class PublicRecipeApiTests(TestCase):
    
    def setUp(self) :
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='test@test.com',password='123456789')
        self.client.force_authenticate(user=self.user)

    def test_retrieve_recipes(self):
        
        sample_recipe(user=self.user)
        
        sample_recipe(user=self.user)
        
        res = self.client.get(RECIPE_URL)
        
        rescipes = Recipe.objects.all().order_by('-id')
        
        serializer = RecipeSerializer(rescipes,many=True)
        
        self.assertEqual(res.data,serializer.data)
        
        self.assertEqual(res.status_code,status.HTTP_200_OK)
    
    def test_recipe_limit_to_auth_user(self):
        
        user2 = get_user_model().objects.create_user(email="test2@test.com",password="12346675656")
        
        sample_recipe(user=self.user)
        
        sample_recipe(user=user2)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user=self.user)
        
        serializer = RecipeSerializer(recipes,many=True)
        
        self.assertEqual(serializer.data,res.data)

        self.assertEqual(res.status_code,status.HTTP_200_OK)

        self.assertEqual(len(res.data),1)
        
        

        




