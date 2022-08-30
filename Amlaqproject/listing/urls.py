from django.urls import path, include
from .views import *

urlpatterns = [
    path('api/', ListingView.as_view({"get": "list", "post": "create", "delete": "destroy", "update": "update"}),
         name='basic_view'),
    path('api/update/<int:pk>/', UpdateUserQuestionView.as_view(), name="update_basic"),
    path('image/', ListMedia.as_view(), name='basic_view'),
    path('image/update/<int:pk>/', ListMediaUdate.as_view(), name="update_basic"),
    path('property/', FindProperty.as_view(), name="get_property"),
    path('find/', filterViewSet.as_view(), name="get_property"),
    # path('post/', AddListingPostData.as_view(), name="post"),
    path('post/', AddListingPostData.as_view({"get": "list", "post": "create", "delete": "destroy", "update": "update"}),
         name='basic_view'),

]
