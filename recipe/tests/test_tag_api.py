from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from django.test import TestCase
from rest_framework.test import APIClient
from core.models import Tag
from recipe.serializers import TagSerialzier

TAG_URL = reverse("recipe:tag-list")

class PublicTagApiTest(TestCase):
    
    def setUp(self) -> None:
        self.client = APIClient()
    
    def login_required_for_get_tags_list(self):
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTest(TestCase):
    
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email="test@test.com",password="12423455785656")
        self.client.force_authenticate(user=self.user)
    
    def test_retrieve_tags(self):
        Tag.objects.create(user=self.user,name="vegan")
        Tag.objects.create(user=self.user,name="Dessert")
        res = self.client.get(TAG_URL)
        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerialzier(tags,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)
    
    def test_tags_is_available_for_auth_users(self):
        user2 = get_user_model().objects.create_user(email="mousa@mouasa.com",password="dsfvcdvhdso")
        Tag.objects.create(user=user2,name="fruity")
        tag = Tag.objects.create(user=self.user,name="Confort Food")
        res = self.client.get(TAG_URL)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data[0]["name"],tag.name)
    
    def test_create_tag_successfully(self):
        payload= {
            "name":"test tag"
        }
        self.client.post(TAG_URL,payload)

        exists = Tag.objects.filter(user=self.user,name=payload["name"]).exists()
        self.assertTrue(exists)
        
    
    def test_create_tag_invalid(self):
        payload= {
            "name":""
        }
        res=self.client.post(TAG_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        exists = Tag.objects.filter(user=self.user,name=payload["name"]).exists()
        self.assertFalse(exists)

    




