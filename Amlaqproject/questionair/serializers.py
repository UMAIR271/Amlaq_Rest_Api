from email.mime import image
from .models import *
from rest_framework import serializers
from loginapp.models import *
from loginapp.serializers import *



class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = question
        fields = '__all__'

class ListingQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingQuestion
        fields = '__all__'


class interestedAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = interestedAnswer
        fields = '__all__'
    

