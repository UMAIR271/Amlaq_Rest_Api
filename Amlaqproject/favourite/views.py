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
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class FavouriteView(APIView):
    serializer_class = FavouriteListingSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (FormParser, MultiPartParser)


    def get(self, request):
        user = request.user.id
        print(user)
        snippet=FavouriteListing.objects.filter(user = user).values()
        return Response(snippet)

    def post(self, request):
        user = request.user.id
        print(user)
        data = request.data
        id = data['listing']
        listing_id =  listing.objects.get(id = id)
        listing_id.is_favourite = True
        listing_id.save()
    
        # request.data._mutable=True
        # data = request.data
        # listing_id =  listing.objects.get(id = listing_id)
        # print(listing_id)

        # data['user'] = user
        # serializer = self.serializer_class(data=data)
        # if  serializer.is_valid(raise_exception=True):
        #     serializer.save()
            
        return Response(listing_id)


class checkfavouaite(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user.id
        print(user)
        snippet=FavouriteListing.objects.filter(user = user).values('status')
        if snippet:
            return Response(snippet, status = status.HTTP_200_OK)
        return Response(status = status.HTTP_404_NOT_FOUND)