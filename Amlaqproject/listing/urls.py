from django.urls import path, include

from . import views
from .views import ListingViewSet

urlpatterns = [
    path('list/', ListingViewSet.as_view({'get': 'list'}), name="list"),
    path('create/noti/', views.CreateNotification.as_view(), name='add_invoie_view'),
]
