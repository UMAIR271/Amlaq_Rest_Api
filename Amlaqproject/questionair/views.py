from django.shortcuts import render
from django.http import Http404
import json
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from django.shortcuts import render
from questionair.serializers import *
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


# Create your views here.
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


