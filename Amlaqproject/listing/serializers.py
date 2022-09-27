from email.mime import image
from .models import *
from rest_framework import serializers
from loginapp.models import *
from loginapp.serializers import *

class Listing_MediaSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)
    image_path = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = Listing_Media
        fields = ('images_Url', 'listing', 'image_path')
    def get_image_url(self, obj):
        return obj.images_Url.url

class verifedImageSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)
    image_path = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = property_verification
        fields = ('propertyVerificationImage', 'listing', 'image_path')
    def get_image_url(self, obj):
        return obj.propertyVerificationImage.url

class floorplaneSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)
    image_url = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = floorPlane
        fields = ('floorPlaneImage', 'listing', 'image_url')
    def get_image_url(self, obj):
        return obj.floorPlaneImage.url

class CompressImageSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)
    # image_url = serializers.SerializerMethodField('get_image_url')
    class Meta:
        print("ser")
        model = compress_image
        fields = '__all__'


class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = '__all__'

class ListingAmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing_Amenities
        fields = '__all__'

class porpertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property_Type
        fields = '__all__'

class getListingSerializer(serializers.ModelSerializer):
    # user = UserProfileSerializer(many=True, read_only=True)
    username = serializers.CharField(
        source="user_name.email", read_only=True)
    list = Listing_MediaSerializer(many=True, read_only=True)
    property = porpertyTypeSerializer(many=True, read_only=True)
    # Amenities = AmenitiesSerializer(many=True, read_only=True)
    floorplane = floorplaneSerializer(many=True, read_only=True)
    propertyVerificationImage = verifedImageSerializer(many=True, read_only=True)

    
    class Meta:
        model = listing
        fields = '__all__'

class filterserializers(serializers.ModelSerializer):
    Amenities = AmenitiesSerializer(many=True, read_only=True)
    class Meta:
        model = Amenities
        fields = '__all__'



class  postListingSerializer(serializers.ModelSerializer):
    list = serializers.StringRelatedField(many=True)
    property = serializers.StringRelatedField(many=True)
    # Amenities_ID = AmenitiesSerializer(many=True)
    # Amenities_ID = serializers.StringRelatedField(many=True)
    
    floorplane = serializers.StringRelatedField(many=True)
    propertyVerificationImage = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = listing
        fields = '__all__'

class interestedListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = interested
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def to_representation(self, instance):
        data = super(AppointmentSerializer, self).to_representation(instance)
        data['user1'] = instance.user1.name
        data['user2'] = instance.user2.name
        data['listing'] = instance.listing.Title
        return data


class SlotstSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableSlots
        fields = '__all__'

    def to_representation(self, instance):
        data = super(SlotstSerializer, self).to_representation(instance)
        data['user'] = instance.user.name
        data['listing'] = instance.listing.Title
        return data
