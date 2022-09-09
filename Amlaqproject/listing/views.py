from email.mime import image
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
from .mypagination import myCursorPagination
from django.http import QueryDict
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend


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
    pagination_class = myCursorPagination

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
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = Listing_MediaSerializer

class ListMediaUdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing_Media.objects.all()
    serializer_class = Listing_MediaSerializer

class FindProperty(APIView):
    serializer_class = ListingSerializer
    def get(self, request):
        try:
            data= request.data
            query = listing.objects.filter(Q(project_name__contains = data['query']) | Q(street_Address__contains = data["query"]))
            print(query)
            serializer = self.serializer_class(query, many = True)
            return Response(serializer.data)
        except listing.DoesNotExist:
            raise Http404

class AmenitiesView(viewsets.ModelViewSet):
    queryset = Amenities.objects.all()
    serializer_class = AmenitiesSerializer
    parser_classes = (FormParser, MultiPartParser)

class UpdateAmenitiesView(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = AmenitiesSerializer

    def get_object(self):
        try:
            return Amenities.objects.get(id=self.kwargs.get('pk'))
        except Amenities.DoesNotExist:
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

class AddListingPostData(APIView):
    serializer_list = ListingSerializer
    serializer_property = porpertyTypeSerializer
    serializer_image = Listing_MediaSerializer
    compress_serializer = CompressImageSerializer
    serializer_Amenities = AmenitiesSerializer
    def post(self, request):
        try:
            images = {}
            Amenities = {}
            property_type = {}
            image = 'images_path'
            Amenities_Name = 'Amenities_Name'
            property_name = 'property_type'
            data= request.data
            for key, value in data.items():
                if image == key:
                    images[key] = value
                if Amenities_Name == key:
                    Amenities[key] = value
                if property_name == key:
                    property_type[key] = value
            data.pop("images_path")
            data.pop("Amenities_Name")
            data.pop("property_type")
            serializer1 = self.serializer_list(data=data)
            serializer1.is_valid(raise_exception=True)
            serializer1.save()
            id=serializer1.data['id']
            images['listing'] = id
            print(images)
            Amenities['listing'] = id
            property_type['listing'] = id
            
            serializer2 = self.serializer_image(data=images)
            serializer2.is_valid(raise_exception=True)
            serializer2.save()
            print(images['listing'])
            print(images)
            compress_image = self.compress_serializer(data=images)
            compress_image.is_valid(raise_exception=True)
            # compress_image.save()

            serializer3 = self.serializer_Amenities(data=Amenities)
            serializer3.is_valid(raise_exception=True)
            serializer3.save()

            serializer4 = self.serializer_property(data=property_type)
            serializer4.is_valid(raise_exception=True)
            serializer4.save()
            return Response(serializer1.data)
        except listing.DoesNotExist:
            raise Http404


class filterViewSet(generics.ListAPIView):
    queryset = listing.objects.all()

    serializer_class = ListingSerializer
    parser_classes = (FormParser, MultiPartParser)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['Purpose_Type','property_pricing','property', 'size','Bedrooms','Batrooms','Project_status']
 

class BasicQuestionView(viewsets.ModelViewSet):
    serializer_class = BasicQuestionSerializer
    queryset = BasicQuestionair.objects.all()


class UpdateQuestionView(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = BasicQuestionSerializer

    def get_object(self):
        try:
            return BasicQuestionair.objects.get(id=self.kwargs.get('pk'))
        except BasicQuestionair.DoesNotExist:
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


class UserQuestionView(viewsets.ModelViewSet):
    serializer_class = UserQuestionSerializer
    queryset = UserQuestionair.objects.all()


class UpdateUserQuestionView(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = UserQuestionSerializer

    def get_object(self):
        try:
            return UserQuestionair.objects.get(id=self.kwargs.get('pk'))
        except UserQuestionair.DoesNotExist:
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


class ListingQuestionView(viewsets.ModelViewSet):
    serializer_class = ListingQuestionSerializer
    queryset = ListingQuestionair.objects.all()


class UpdateListingQuestionView(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = ListingQuestionSerializer

    def get_object(self):
        try:
            return ListingQuestionair.objects.get(id=self.kwargs.get('pk'))
        except ListingQuestionair.DoesNotExist:
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


class FavouriteLisitingView(viewsets.ModelViewSet):
    serializer_class = FavouriteListingSerializer
    queryset = FavouriteListing.objects.all()


class UpdateFavouriteView(generics.UpdateAPIView):
    queryset = FavouriteListing.objects.all()
    serializer_class = FavouriteListingSerializer

    def get(self, request, pk):
        snippet = self.get_object()
        serializer = self.serializer_class(snippet)
        return Response(serializer.data)


class AppointmentView(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()


class UpdateAppointmentView(generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get(self, request, pk):
        snippet = self.get_object()
        serializer = self.serializer_class(snippet)
        return Response(serializer.data)


class SlotsView(viewsets.ModelViewSet):
    serializer_class = SlotstSerializer
    queryset = AvailableSlots.objects.all()


class UpdateSlotsView(generics.UpdateAPIView):
    queryset = AvailableSlots.objects.all()
    serializer_class = SlotstSerializer

    def get(self, request, pk):
        snippet = self.get_object()
        serializer = self.serializer_class(snippet)
        return Response(serializer.data)