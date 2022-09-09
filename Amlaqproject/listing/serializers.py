from email.mime import image
from .models import *
from rest_framework import serializers

class Listing_MediaSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)
    image_url = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = Listing_Media
        fields = ('images_path', 'listing', 'image_url')
    def get_image_url(self, obj):
        return obj.images_path.url

class CompressImageSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)
    # image_url = serializers.SerializerMethodField('get_image_url')
    class Meta:
        print("ser")
        model = compress_image
        fields = '__all__'




# class AddListingSerializer(serializers.ModelSerializer):
#     print("heloo")
#     list = ListingSerializer(many=True)
#     print(list)
#     # Amenities = GenreSerializer(many=True)
#     class Meta:
#         print("hell")
#         model = listing
#         fields = ['user_name','Title','Descriptions','Type','Purpose_Type',
#         'Property_Type','Bedrooms','Batrooms','Furnishing_type','Property_Tenure',
#         'size','Build_up_Area','parking_number','Property_Developer','Build_year','Building_Floor',
#         'Floor_number','Dewa_number','Occupancy','Project_status','Renovation_type','Layout_type',
#         'property_pricing','Service_charge','financial_status','Cheques','property_location','street_Address',
#         'project_name','list']

#     def create(self, validated_data):
#         print(validated_data)
#         images = validated_data.pop('list')
#         list = listing.objects.create(**validated_data)
#         for image in images:
#             Listing_Media.objects.create(**image, listing = list)
#         return   list  

class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = '__all__'


class porpertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property_Type
        fields = '__all__'

class ListingSerializer(serializers.ModelSerializer):
    list = serializers.StringRelatedField(many=True)
    compress = serializers.StringRelatedField(many=True)
    property = serializers.StringRelatedField(many=True)
    Amenities = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = listing
        fields = '__all__'




# class NotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = notifications
#         fields = '__all__'


class BasicQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicQuestionair
        fields = '__all__'


class UserQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuestionair
        fields = '__all__'


class ListingQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingQuestionair
        fields = '__all__'


class FavouriteListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteListing
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
