from django.urls import path, include

from . import views
from .views import ListingViewSet

urlpatterns = [
    path('list/', ListingViewSet.as_view({'get': 'list'}), name="list"),
    path('create/noti/', views.CreateNotification.as_view(), name='add_invoie_view'),
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
]
