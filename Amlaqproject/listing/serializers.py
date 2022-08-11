from .models import listing
from rest_framework import serializers



class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = listing
        fields = '__all__'