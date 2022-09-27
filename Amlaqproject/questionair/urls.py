from django.urls import path, include
from listing.views import *
from . import views
urlpatterns = [
#     path('userlisting/', userListingView.as_view({"get": "list", "post": "create", "delete": "destroy","update": "update"}), name='basic_view'),
    path('basic/question/', views.BasicQuestionView.as_view({"get": "list", "post": "create"}), name='basic_view'),
    path('update/basic/<int:pk>/', views.UpdateQuestionView.as_view(), name="update_basic"),
    path('user/question/', views.UserQuestionView.as_view({"get": "list", "post": "create"}), name='user_question_view'),
    path('update/user/question/<int:pk>/', views.UpdateUserQuestionView.as_view(), name="update_user_question"),

    path('listing/question/', views.ListingQuestionView.as_view({"get": "list", "post": "create"}), name='listing_question_view'),

    path('update/listing/<int:pk>/', views.UpdateListingQuestionView.as_view(), name="update_listing_question"),

    
]
