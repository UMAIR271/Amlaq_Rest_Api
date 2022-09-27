from email.mime import image
from .models import *
from rest_framework import serializers
from loginapp.models import *
from loginapp.serializers import *



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

