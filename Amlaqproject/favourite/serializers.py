from email.mime import image
from .models import *
from rest_framework import serializers
from loginapp.models import *
from loginapp.serializers import *




class FavouriteListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteListing
        fields = '__all__'

