from django.shortcuts import render
from django.shortcuts import render
from django.http import Http404
import json
from django.shortcuts import get_object_or_404
# Create your views here.
from rest_framework import status
from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from django.shortcuts import render
from .serializers import *
from django.db.models import Q
from listing.models import listing
from rest_framework import viewsets
from rest_framework.response import Response
from .mypagination import myCursorPagination
from django.db.models import Max
from .models import *
from django.http import QueryDict
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class FavouriteLisitingView(viewsets.ModelViewSet):
    serializer_class = FavouriteListingSerializer
    queryset = FavouriteListing.objects.all()
    parser_classes = (FormParser, MultiPartParser)



class UpdateFavouriteView(generics.UpdateAPIView):
    queryset = FavouriteListing.objects.all()
    serializer_class = FavouriteListingSerializer
    parser_classes = (FormParser, MultiPartParser)


    def get(self, request, pk):
        snippet = self.get_object()
        serializer = self.serializer_class(snippet)
        return Response(serializer.data)

