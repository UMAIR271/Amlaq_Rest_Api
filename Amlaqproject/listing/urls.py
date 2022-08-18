from django.urls import path, include
from listing.views import ListingViewSet

urlpatterns = [
    path('list/', ListingViewSet.as_view() , name= "list"),
]