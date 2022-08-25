from .models import listing, notifications, BasicQuestionair, UserQuestionair, ListingQuestionair
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

