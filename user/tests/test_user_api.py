from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")

def create_user(**params):
  return get_user_model().objects.create_user(**params)

class PublicUserApiTest(TestCase):
  """ test user api public"""
  def setUp(self) :
    self.client = APIClient()
    self.payload =  {
        "email":"200mousa@gmail.com",
        "password":"123456789",
        "name":"mousa"
      }
  
  def test_create_valid_user_success(self):
      """test create user with valid self.payload """
  
      res = self.client.post(CREATE_USER_URL,self.payload)
      self.assertEqual(res.status_code,status.HTTP_201_CREATED)
      self.assertEqual(res.data["email"],self.payload["email"])
      self.assertEqual(res.data["name"],self.payload["name"])
      user = get_user_model().objects.get(**res.data)
      self.assertTrue(user.check_password(self.payload["password"]))
      self.assertNotIn("password",res.data)
  
  
  
  def test_creating_user_already_exists(self):
    
    create_user(**self.payload)
    res = self.client.post(CREATE_USER_URL,self.payload)
    self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
  
  

  def test_is_password_is_less_than_8(self):
    payload = {
        "email":"200mousa@gmail.com",
        "password":"1234",
        "name":"mousa"
      }
    res = self.client.post(CREATE_USER_URL,payload)
    
    self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
    
    is_user_exists = get_user_model().objects.filter(email=self.payload["email"]).exists()

    self.assertFalse(is_user_exists)

  
  def test_create_token_for_user(self):
      create_user(**self.payload)
      res = self.client.post(TOKEN_URL,self.payload)
      print(res.data)
      self.assertIn("token",res.data)
      self.assertEqual(res.status_code,status.HTTP_200_OK)
  
  
  def test_create_token_for_invalid_credentails(self):
      create_user(email="200mousa@gmail.com",password="12345678912345")
      res = self.client.post(TOKEN_URL,self.payload)
      self.assertNotIn("token",res.data)
      self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
  
  def test_create_token_for_not_exits_user(self):
      res = self.client.post(TOKEN_URL,self.payload)
      self.assertNotIn("token",res.data)
      self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

  def test_empty_credentials(self):
      res = self.client.post(TOKEN_URL,{})
      self.assertNotIn("token",res.data)
      self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)