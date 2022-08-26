from django.shortcuts import render
from django.http import Http404
import json
from django.shortcuts import get_object_or_404
# Create your views here.
from rest_framework import status
from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from django.shortcuts import render
from listing.serializers import *
from django.db.models import Q
from listing.models import listing
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.


# class ListingModelViewSets(viewsets.ModelViewSet):
#     queryset = listing.objects.all()
#     serializer_class = ListingSerializer

# class ListingViewSet(viewsets.ViewSet):
#     """
#     A viewset for viewing and editing user instances.
#     """
#     serializer_class = ListingSerializer
#     queryset = listing.objects.all()

class ListingViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """

    def list(self, request):
        queryset = listing.objects.all()
        serializer = ListingSerializer(queryset, many=True)
        return Response(serializer.data)
        
    def retrieve(self, request, pk=None):
        try:
            snippet = listing.objects.get(pk=pk)
        except listing.DoesNotExist:
            print("rest")
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ListingSerializer(snippet)
        return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = ListingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            snippet = listing.objects.get(pk=pk)
        except listing.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ListingSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def partial_update(self, request, pk=None):
    #     pass

    def destroy(self, request, pk=None):
        try:
            snippet = listing.objects.get(pk=pk)
        except listing.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ListingView(viewsets.ModelViewSet):
    queryset = listing.objects.all()
    serializer_class = ListingSerializer
    parser_classes = (FormParser, MultiPartParser)

class UpdateUserQuestionView(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = ListingSerializer

    def get_object(self):
        try:
            return listing.objects.get(id=self.kwargs.get('pk'))
        except listing.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        snippet = self.get_object()
        serializer = self.serializer_class(snippet)
        return Response(serializer.data)

    def put(self, request, pk):
        object = self.get_object()
        serializer = self.serializer_class(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListMedia(generics.ListCreateAPIView):
    queryset = Listing_Media.objects.all()
    serializer_class = Listing_MediaSerializer

class ListMediaUdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing_Media.objects.all()
    serializer_class = Listing_MediaSerializer

class FindProperty(APIView):
    serializer_class = ListingSerializer
    def get(self, request):
        try:
            data= request.data
            if 'project_name' in str(data):
                query = listing.objects.filter(project_name__contains = data['project_name'])
                print(query)
                serializer = self.serializer_class(query, many = True)
                return Response(serializer.data)
            elif 'street_Address' in str(data):
                query = listing.objects.filter(street_Address__contains = data["street_Address"])
                print(query)
                serializer = self.serializer_class(query, many = True)
                return Response(serializer.data)
            else:
                raise Http404
        except listing.DoesNotExist:
            raise Http404
    

class filterViewSet(generics.ListAPIView):
    queryset = listing.objects.all()
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['Type','Bedrooms','Property_Type', 'project_name','street_Address']
