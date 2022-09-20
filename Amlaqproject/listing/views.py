from email.mime import image
from tkinter import image_names
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
from django.db.models import Max
from loginapp.models import *
from django.http import QueryDict
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .helper import *


# class userListingView(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = userListingSerializers
#     parser_classes = (FormParser, MultiPartParser)
#     pagination_class = myCursorPagination

class ListingView(viewsets.ModelViewSet):
    queryset = listing.objects.all()
    serializer_class = getListingSerializer
    parser_classes = (FormParser, MultiPartParser)
    pagination_class = myCursorPagination

class GetListingView(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = getListingSerializer

    def get_object(self):
        try:
            return listing.objects.get(id=self.kwargs.get('pk'))
        except listing.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        print("hello")
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

class FindProperty(viewsets.ModelViewSet):
    serializer_class = getListingSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query')
        try:
                query = listing.objects.filter(Q(project_name__contains = query) | Q(street_Address__contains = query))
                return query

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
    serializer_list = postListingSerializer
    serializer_property = porpertyTypeSerializer
    serializer_image = Listing_MediaSerializer
    compress_serializer = CompressImageSerializer
    floorplane_serializer = floorplaneSerializer
    serializer_Amenities = AmenitiesSerializer
    verifed_serializer = verifedImageSerializer

    parser_classes = (FormParser, MultiPartParser)
    
    def post(self, request):
        try:
            arr = []
            Amenities = ""
            images = ""
            floorPlaneImages = ""
            property = ""
            verify_images = ""
            data= request.data
            if 'images_Url' in str(data):
                images = dict((request.data).lists())['images_Url']
                data.pop("images_Url")
            else:
                 return Response({"message":"enter the image"}, status=status.HTTP_400_BAD_REQUEST)
            if 'floorPlaneImage' in str(data):
                floorPlaneImages = dict((request.data).lists())['floorPlaneImage']
                data.pop("floorPlaneImage")
            else:
                pass

            if 'Amenities_Name' in str(data):
                Amenities = dict((request.data).lists())['Amenities_Name']
                data.pop("Amenities_Name")

            else:
                pass
            if 'property_type' in str(data):
                property = request.data['property_type']
                data.pop("property_type")

            else:
                pass
            if 'propertyVerificationImage' in str(data):
                verify_images = dict((request.data).lists())['propertyVerificationImage']
                data.pop("propertyVerificationImage")
            else:
                pass

            
            if data:
                serializer1 = self.serializer_list(data=data)
                if  serializer1.is_valid(raise_exception=True):
                    serializer1.save()
                    id=serializer1.data['id']
                else:
                        return Response({"message":"enter the listing"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                        return Response({"message":"enter the listing"}, status=status.HTTP_400_BAD_REQUEST)
                
            if images:
                for img_name in images:
                    modified_data = modify_input_for_multiple_files(id,img_name)
                    file_serializer =self.serializer_image(data=modified_data)
                    if file_serializer.is_valid(raise_exception=True):
                        file_serializer.save()
                        arr.append(file_serializer.data)
                    else:
                        print("umair")
                        return Response({"message":"enter the image"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                pass
            if Amenities:            
                for Amenities_name in Amenities:
                    modified_data = multiple_Amenaties(id,Amenities_name)
                    file_serializer =self.serializer_Amenities(data=modified_data)
                    if file_serializer.is_valid(raise_exception=True):
                        file_serializer.save()
                        arr.append(file_serializer.data)
                    else:
                        return Response({"message":"enter the Amenities"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                pass
                # return Response({"message":"enter the Amenities"}, status=status.HTTP_400_BAD_REQUEST)

            if property:
                modified_data = multiple_property(id,property)
                file_serializer =self.serializer_property(data=modified_data)
                if file_serializer.is_valid():
                    file_serializer.save()
                    arr.append(file_serializer.data)
                else:
                    return Response({"property":"enter the Property Name"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                pass
                    # return Response({"property":"enter the Property Name"}, status=status.HTTP_400_BAD_REQUEST)
            
            if floorPlaneImages:
                for floorImage in floorPlaneImages:
                    modified_data = floorPlans_multiple_files(id,floorImage)
                    print(modified_data)
                    file_serializer =self.floorplane_serializer(data=modified_data)
                    if file_serializer.is_valid():
                        file_serializer.save()
                        arr.append(file_serializer.data)
                    else:
                        return Response({"message":"enter the floor Plane Image"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                pass
                # return Response({"message":"enter floor the image"}, status=status.HTTP_400_BAD_REQUEST)

            if verify_images:
                for verify_image in verify_images:
                    modified_data = verify_multiple_files(id,verify_image)
                    file_serializer =self.verifed_serializer(data=modified_data)
                    if file_serializer.is_valid():
                        file_serializer.save()
                        arr.append(file_serializer.data)
                    else:
                        return Response({"message":"enter the verify Plane Image"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                pass


            return Response({"listing_id":id},status=status.HTTP_200_OK)
        except listing.DoesNotExist:
            raise Http404


class filterViewSet(generics.ListAPIView):
    queryset = listing.objects.all()
    serializer_class = filterserializers
    parser_classes = (FormParser, MultiPartParser)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['Purpose_Type','Type','property_pricing','property', 'size','Bedrooms','Batrooms','Project_status','Amenities__Amenities_Name']
 

class BasicQuestionView(viewsets.ModelViewSet):
    serializer_class = BasicQuestionSerializer
    parser_classes = (FormParser, MultiPartParser)
    queryset = BasicQuestionair.objects.all()


class UpdateQuestionView(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = BasicQuestionSerializer
    parser_classes = (FormParser, MultiPartParser)


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
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = UserQuestionSerializer
    queryset = UserQuestionair.objects.all()


class UpdateUserQuestionView(APIView):
    # permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser)
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
    parser_classes = (FormParser, MultiPartParser)


class UpdateListingQuestionView(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = ListingQuestionSerializer
    parser_classes = (FormParser, MultiPartParser)

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
    parser_classes = (FormParser, MultiPartParser)



class UpdateFavouriteView(generics.UpdateAPIView):
    queryset = FavouriteListing.objects.all()
    serializer_class = FavouriteListingSerializer
    parser_classes = (FormParser, MultiPartParser)


    def get(self, request, pk):
        snippet = self.get_object()
        serializer = self.serializer_class(snippet)
        return Response(serializer.data)

class interestedLisitingView(viewsets.ModelViewSet):
    serializer_class = interestedListingSerializer
    queryset = interested.objects.all()
    parser_classes = (FormParser, MultiPartParser)



class getInterestedLisitingView(generics.UpdateAPIView):
    queryset = interested.objects.all()
    serializer_class = interestedListingSerializer
    parser_classes = (FormParser, MultiPartParser)


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

class filterView(generics.ListAPIView):
    model = listing
    serializer_class = getListingSerializer
    parser_classes = (FormParser, MultiPartParser)


    # Show all of the PASSENGERS in particular WORKSPACE
    # or all of the PASSENGERS in particular AIRLINE
    def get_queryset(self):
        try:
            queryset = listing.objects.all()
            check_Purpose_Type = self.request.query_params.get('check_Purpose_Type', None)
            check_Type = self.request.query_params.get('check_Type', None)
            check_property_Type = self.request.query_params.get('check_property_Type', None)
            min_price = self.request.query_params.get('min_price', None)
            max_price = self.request.query_params.get('max_price', None)
            check_property_size = self.request.query_params.get('check_property_size', None)
            check_bedroom = self.request.query_params.get('check_bedroom', None)
            check_batroom = self.request.query_params.get('check_batroom')
            check_project_status = self.request.query_params.get('check_project_status', None)
            check_Amenities = self.request.query_params.get('check_Amenities', None)

            if check_Purpose_Type:
                queryset = queryset.filter(Purpose_Type=check_Purpose_Type)
            if check_Type:
                queryset = queryset.filter(Type=check_Type)
            if check_property_Type:
                queryset = queryset.filter(property__property_type=check_property_Type)
            if min_price == '':
                min_price = 0
            if min_price == '':
                queryset = queryset.all().aggregate(Max('property_pricing'))
            if min_price and max_price:
                queryset = queryset.filter(property_pricing__range=(min_price,max_price))
            if check_property_size:
                queryset = queryset.filter(size=check_property_size)
            if check_bedroom:
                queryset = queryset.filter(Bedrooms=check_bedroom)
            if check_batroom:
                queryset = queryset.filter(Batrooms=check_batroom)
            if check_project_status:
                queryset = queryset.filter(Project_status=check_project_status)
            if check_Amenities:
                queryset = queryset.filter(Amenities__Amenities_Name=check_Amenities)
            return queryset
        except listing.DoesNotExist:
            raise Http404




class UpdateSlotsView(generics.UpdateAPIView):
    queryset = AvailableSlots.objects.all()
    serializer_class = SlotstSerializer

    def get(self, request, pk):
        snippet = self.get_object()
        serializer = self.serializer_class(snippet)
        return Response(serializer.data)