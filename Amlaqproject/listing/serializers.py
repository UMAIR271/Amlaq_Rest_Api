from .models import *
from rest_framework import serializers



# class ListingSerializer(serializers.ModelSerializer):
#     # list = serializers.StringRelatedField(many=True)
#     # Amenities = serializers.StringRelatedField(many=True)
#     class Meta:
#         model = listing
#         fields = '__all__'

class ListingSerializer(serializers.ModelSerializer):
    list = serializers.StringRelatedField(many=True)
    Amenities = serializers.StringRelatedField(many=True)
    class Meta:
        model = listing
        fields = '__all__'


class Listing_MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing_Media
        fields = '__all__'


class Property_NameSerializer(serializers.Serializer):
     name = serializers.CharField()
    #  Address = serializers.CharField()

