from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

def sample_user(email="test@test.com",password="testtest1234"):
  return get_user_model().objects.create_user(email=email,password=password)


class TestModel(TestCase):
  def test_user_create_email_password(self):
    email="test@test.com"
    password="testtest"
    user = get_user_model().objects.create_user(
      email=email,
      password=password
    )
    self.assertEqual(user.email,email)
    self.assertTrue(user.check_password(password))
  
  def test_user_create_email_email_normalized(self):
    email="test@TEST.com"
    password="testtest"
    user = get_user_model().objects.create_user(
      email=email,
      password=password
    )
    self.assertEqual(user.email,email.lower())
  
  def test_create_user_with_invalid_email(self):
    with self.assertRaises(ValueError):
      email=None
      password="testtest"
      user = get_user_model().objects.create_user(
        email=email,
        password=password
      )
  
  def test_create_super_user(self):
    email="test@test.com"
    password="testtest"
    user = get_user_model().objects.create_superuser(
      email=email,
      password=password,
    )
    self.assertEqual(user.email,email)
    self.assertTrue(user.check_password(password))
  
  def test_is_user_user(self):
    email="test@test.com"
    password="testtest"
    user = get_user_model().objects.create_superuser(
      email=email,
      password=password,
    )
    self.assertTrue(user.is_staff)
    self.assertTrue(user.is_superuser)

  def test_tag_str_representation(self):
    tag = models.Tag.objects.create(
      user=sample_user(),
      name='vegan'
    )
    self.assertEqual(str(tag),tag.name)

  def test_ingredient_str(self):
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name="Cucumber"
        )
        self.assertEqual(str(ingredient),ingredient.name)
  
  def test_recipe_str(self):
    recipe = models.Recipe.objects.create(
      user=sample_user(),
      title="Steak and mushroom sauce",
      time_minutes=5,
      price=5.00,
    )
    self.assertEqual(str(recipe),recipe.title)