from django.urls import path, include
from  .views import *
from . import views
urlpatterns = [
#     path('userlisting/', userListingView.as_view({"get": "list", "post": "create", "delete": "destroy","update": "update"}), name='basic_view'),
    
    path('favourite/listing/',
         views.FavouriteLisitingView.as_view({"get": "list", "post": "create"}), name='favourite_listing'),

    path('update/favourite/<int:pk>/', views.UpdateFavouriteView.as_view(), name="update_favourite_listing"),

    
    
]
