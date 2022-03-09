from http import client
from django.contrib.auth import get_user_model
from django.urls import reverse 
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status 
from recipe.serializers import  IngredientSerialzier
from core.models import Ingredient

INGREDIENT_URL = reverse('recipe:ingredient-list')

class PublicIngredientTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        res=self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)



class PrivateIngredientTests(TestCase):
    
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email="test@test.com",password="123456789")
        self.client.force_authenticate(user=self.user)
    
    def test_retrieve_ingredient_list(self):
        Ingredient.objects.create(user=self.user,name="Kale")
        Ingredient.objects.create(user=self.user,name="Salt")
        res = self.client.get(INGREDIENT_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerialzier(ingredients,many=True)
        self.assertEqual(res.data,serializer.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
    
    def test_ingredient_limited_to_auth_users(self):
        user2 = get_user_model().objects.create_user(email="test2@gmail.com",password="1234545tr")
        ingredient=Ingredient.objects.create(user=self.user,name="Kale")
        Ingredient.objects.create(user=user2,name="Kale2")
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]["name"],ingredient.name)
    
    def test_create_ingredient_successfully(self):
        payload = {'name':'Cabbage'}
        res= self.client.post(INGREDIENT_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        self.assertTrue(Ingredient.objects.filter(user_id=self.user.id,name=payload["name"]).exists())
        self.assertEqual(res.data['name'],payload['name'])
    
    def test_create_ingredient_invalid(self):
        payload = {'name':''}
        res= self.client.post(INGREDIENT_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Ingredient.objects.filter(user=self.user,name=payload["name"]).exists())



