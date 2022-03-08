from django.db import models
from django.contrib.auth.models import (BaseUserManager
,AbstractBaseUser,PermissionsMixin)
from django.conf import settings
# Create your models here.


class UserManger(BaseUserManager):
    
    def create_user(self,email,password=None,**extra_fields):
      """ create and save new user  """
      if not email:
        raise ValueError("email must be provided")
      user = self.model(email=self.normalize_email(email),**extra_fields)
      user.set_password(password)
      user.save(using=self._db)
      return user 
    
    def create_superuser(self,email,password=None):
      """ create and save new super user """
      user = self.create_user(email,password)
      user.is_staff = True 
      user.is_superuser = True 
      user.save(using=self._db)
      return user 
    


class User(AbstractBaseUser,PermissionsMixin):
    """custom user model """
    email =models.EmailField(max_length=255,unique=True,db_index=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects=UserManger()
    USERNAME_FIELD='email'

class Tag(models.Model):
  name = models.CharField(max_length=255)
  user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="userTags",on_delete=models.CASCADE)
  
  def __str__(self) -> str:
      return self.name