from django.urls import path, include
from listing.views import *
from . import views
urlpatterns = [
    path('basic/question/', views.getQuestionView.as_view(), name="update_basic"),
    path('answer/', views.ListingAnswer.as_view(), name='user_question_view'),
    path('interested/', views.InterestedAnswer.as_view(), name='interested_view'),    
]
