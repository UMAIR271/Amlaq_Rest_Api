from .models import listing, notifications, BasicQuestionair, UserQuestionair, ListingQuestionair, FavouriteListing, \
    Appointment, AvailableSlots
from rest_framework import serializers


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = listing
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = notifications
        fields = '__all__'


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
