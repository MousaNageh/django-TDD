from django.contrib import admin

from core.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from core.models import Tag,Ingredient
# Register your models here.

class UserAdmin(BaseUserAdmin):
  ordering =['id']
  list_display = ['email','name']
  fieldsets = (
      (_("auth info"), {"fields": ('email','password'),}),
      (_("personal info"),{"fields":("name",)}),
      (_("permissions"),{"fields":("is_active","is_staff","is_superuser")}),
      (_("important dates"),{"fields":("last_login",)}),
  )
  add_fieldsets =(
    (None,{
      "classes":("wide",),
      "fields":("email","password1","password2")
    }),
  )
  

admin.site.register(User,UserAdmin) 

#tags
admin.site.register(Tag)
admin.site.register(Ingredient)