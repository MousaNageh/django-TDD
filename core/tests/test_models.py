from django.test import TestCase
from django.contrib.auth import get_user_model

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