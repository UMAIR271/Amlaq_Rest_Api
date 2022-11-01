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




class getQuestionView(APIView):
    serializer_class = QuestionSerializer
    parser_classes = (FormParser, MultiPartParser)


    def get_object(self):
        try:
            return question.objects.get(id=self.kwargs.get('pk'))
        except question.DoesNotExist:
            raise Http404

    def get(self, request):
        try:
            question_list = {}
        # snippet = self.get_object()
            question_type = "Rental Listings"
            Rental_Listings = question.objects.filter(question_type = question_type).values()
            question_list['Rental Listings'] = Rental_Listings
            question_type = "Sales Listings"
            Sales_Listings = question.objects.filter(question_type = question_type).values()
            question_list['Sales Listings'] = Sales_Listings
            print(Sales_Listings)
            # serializer = self.serializer_class(snippet)
            return Response(question_list)
        except question.DoesNotExist:
            raise Http404
        


class ListingAnswer(APIView):
    serializer_class = ListingQuestionSerializer
    # parser_classes = (FormParser, MultiPartParser)


    def post(self, request):
        try:
            question_list = {}
            data = request.data
            question = data['question']
            listing = data['listing']
            for i in question:
                question_list['question'] = i['id']
                question_list['listing'] = listing
                question_list['expected_Answer'] = i['ans']
                serializer = self.serializer_class(data=question_list)
                # print(serializer.data)
                if  serializer.is_valid(raise_exception=True):
                    serializer.save() 
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data)
        except ListingQuestion.DoesNotExist:
            raise Http404



class InterestedAnswer(APIView):
    serializer_class = interestedAnswerSerializer
    # parser_classes = (FormParser, MultiPartParser)
    def post(self, request):
        try:
            interested_list = {}
            data = request.data
            question = data['question']
            listing = data['listing']
            owner_id = data['owner_id']
            user_id = data['user_id']
            future_ans = data['future_ans']
            for i in question:
                interested_list['question'] = i['id']
                interested_list['choice_text'] = i['ans']
                interested_list['listing'] = listing
                interested_list['owner_id'] = owner_id
                interested_list['user_id'] = user_id
                interested_list['save_in_future'] = future_ans
                serializer = self.serializer_class(data=interested_list)
                if  serializer.is_valid(raise_exception=True):
                    serializer.save() 
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                    
            return Response(status=status.HTTP_201_CREATED)
        except interestedAnswer.DoesNotExist:
            raise Http404
