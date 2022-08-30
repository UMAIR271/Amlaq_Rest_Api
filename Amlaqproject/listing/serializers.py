from email.mime import image
from .models import *
from rest_framework import serializers



class ListingSerializer(serializers.ModelSerializer):
    # list = serializers.StringRelatedField(many=True)
    # Amenities = serializers.StringRelatedField(many=True)
    class Meta:
        model = listing
        fields = '__all__'



class Listing_MediaSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)
    class Meta:
        model = Listing_Media
        fields = '__all__'

class AddListingSerializer(serializers.ModelSerializer):
    list = ListingSerializer(many=True)
    # Amenities = GenreSerializer(many=True)
    class Meta:
        model = Listing_Media
        fields = ["images_path", "list"]

    def create(self, validated_data):
        print(validated_data)
        images = validated_data.pop('list')
        list = listing.objects.create(**validated_data)
        for image in images:
            Listing_Media.objects.create(**image, listing = list)
        return   list  
