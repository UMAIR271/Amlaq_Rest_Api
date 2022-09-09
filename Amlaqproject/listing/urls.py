from django.urls import path, include
from listing.views import *
from . import views
urlpatterns = [
    path('api/', ListingView.as_view({"get": "list", "post": "create", "delete": "destroy","update": "update"}), name='basic_view'),
    path('api/update/<int:pk>/', UpdateUserQuestionView.as_view(),              ),
    path('image/', ListMedia.as_view(),name='basic_view'),
    path('image/update/<int:pk>/', ListMediaUdate.as_view(),name="update_basic"),
    path('amenities/', AmenitiesView.as_view({"get": "list", "post": "create", "delete": "destroy","update": "update"}), name='basic_view'),
    path('amenities/update/<int:pk>/', UpdateAmenitiesView.as_view(), name="update_basic"),
    path('property/', FindProperty.as_view(),name="get_property"),
    path('filter/', filterViewSet.as_view(),name="get_property"),
    path('post/', AddListingPostData.as_view(),name="post"),
    path('basic/question/', views.BasicQuestionView.as_view({"get": "list", "post": "create", "delete": "destroy",
                                                             "update": "update"}), name='basic_view'),
    path('update/basic/<int:pk>/', views.UpdateQuestionView.as_view(), name="update_basic"),
    path('user/question/', views.UserQuestionView.as_view({"get": "list", "post": "create", "delete": "destroy",
                                                           "update": "update"}), name='user_question_view'),
    path('update/user/question/<int:pk>/', views.UpdateUserQuestionView.as_view(), name="update_user_question"),

    path('listing/question/', views.ListingQuestionView.as_view({"get": "list", "post": "create", "delete": "destroy",
                                                                 "update": "update"}), name='listing_question_view'),

    path('update/listing/<int:pk>/', views.UpdateListingQuestionView.as_view(), name="update_listing_question"),

    path('favourite/listing/',
         views.FavouriteLisitingView.as_view({"get": "list", "post": "create", "delete": "destroy",
                                              "update": "update"}), name='favourite_listing'),

    path('update/favourite/<int:pk>/', views.UpdateFavouriteView.as_view(), name="update_favourite_listing"),

    path('appointment/',
         views.AppointmentView.as_view({"get": "list", "post": "create", "delete": "destroy",
                                        "update": "update"}), name='appointment'),

    path('update/appointment/<int:pk>/', views.UpdateAppointmentView.as_view(), name="update_favourite_listing"),

    path('slots/',
         views.SlotsView.as_view({"get": "list", "post": "create", "delete": "destroy",
                                  "update": "update"}), name='slots'),

    path('update/slots/<int:pk>/', views.UpdateSlotsView.as_view(), name="update_slots"),



    
]
