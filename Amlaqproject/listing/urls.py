from django.urls import path, include
from listing.views import *
from . import views
urlpatterns = [
#     path('userlisting/', userListingView.as_view({"get": "list", "post": "create", "delete": "destroy","update": "update"}), name='basic_view'),

    path('get/', ListingView.as_view({"get": "list"}), name='basic_view'),
    path('get/<int:pk>/', GetListingView.as_view(), name='basic_view'),
    path('post/', AddListingPostData.as_view(),name="post"),
    path('image/', ListMedia.as_view(),name='basic_view'),
    path('image/update/<int:pk>/', ListMediaUdate.as_view(),name="update_basic"),
    path('amenities/', AmenitiesView.as_view({"get": "list", "post": "create"}), name='basic_view'),
    path('amenities/update/<int:pk>/', UpdateAmenitiesView.as_view(), name="update_basic"),
    path('Listing_amenities/', ListingAmenitiesView.as_view({"get": "list", "post": "create"}), name='basic_view'),

    path('property/', FindProperty.as_view({"get": "list"}),name="get_property"),
    path('filter/', filterView.as_view(),name="get_property"),
    path('mylisting/', MylistingView.as_view(),name="get_property"),
#     path('basic/question/', views.BasicQuestionView.as_view({"get": "list", "post": "create"}), name='basic_view'),
#     path('update/basic/<int:pk>/', views.UpdateQuestionView.as_view(), name="update_basic"),
#     path('user/question/', views.UserQuestionView.as_view({"get": "list", "post": "create"}), name='user_question_view'),
#     path('update/user/question/<int:pk>/', views.UpdateUserQuestionView.as_view(), name="update_user_question"),

#     path('listing/question/', views.ListingQuestionView.as_view({"get": "list", "post": "create"}), name='listing_question_view'),

#     path('update/listing/<int:pk>/', views.UpdateListingQuestionView.as_view(), name="update_listing_question"),

#     path('favourite/listing/',
#          views.FavouriteLisitingView.as_view({"get": "list", "post": "create"}), name='favourite_listing'),

#     path('update/favourite/<int:pk>/', views.UpdateFavouriteView.as_view(), name="update_favourite_listing"),

#     path('interested/listing/',
#          views.interestedLisitingView.as_view({"get": "list", "post": "create"}), name='favourite_listing'),
#     path('get/interested/<int:pk>/', views.getInterestedLisitingView.as_view(), name="update_favourite_listing"),


#     path('appointment/',
#          views.AppointmentView.as_view({"get": "list", "post": "create"}), name='appointment'),

#     path('update/appointment/<int:pk>/', views.UpdateAppointmentView.as_view(), name="update_favourite_listing"),

#     path('slots/',
#          views.SlotsView.as_view({"get": "list", "post": "create"}), name='slots'),

#     path('update/slots/<int:pk>/', views.UpdateSlotsView.as_view(), name="update_slots"),



    
]
