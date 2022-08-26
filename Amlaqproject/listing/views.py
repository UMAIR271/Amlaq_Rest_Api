from django.http import Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404
# Create your views here.
from rest_framework import status, generics
from django.shortcuts import render
from rest_framework.views import APIView

from .serializers import ListingSerializer, NotificationSerializer, BasicQuestionSerializer, UserQuestionSerializer, \
    ListingQuestionSerializer, FavouriteListingSerializer
from .models import listing, notifications, BasicQuestionair, UserQuestionair, ListingQuestionair, FavouriteListing
from rest_framework import viewsets
from rest_framework.response import Response


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


class CreateNotification(generics.ListCreateAPIView):
    queryset = notifications.objects.all()
    serializer_class = NotificationSerializer


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
