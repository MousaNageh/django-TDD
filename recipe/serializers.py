from rest_framework import serializers
from core.models import Tag,Ingredient

class TagSerialzier(serializers.ModelSerializer):

    class Meta:
        model=Tag
        fields = ("id","name")
        read_only_fields = ("id",)
        

class IngredientSerialzier(serializers.ModelSerializer):
    class Meta:
        model=Ingredient
        fields = ("id","name")
        read_only_fields = ("id",)