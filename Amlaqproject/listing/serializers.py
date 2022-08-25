from .models import listing, notifications
from rest_framework import serializers



class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = listing
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = notifications
        fields = '__all__'
