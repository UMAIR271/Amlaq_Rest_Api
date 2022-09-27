from django.db import models
from listing.models import listing
# Create your models here.
class BasicQuestionair(models.Model):
    title = models.CharField(max_length=100)
    answer_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class UserQuestionair(models.Model):
    question = models.ForeignKey(BasicQuestionair, on_delete=models.CASCADE)
    answer1 = models.CharField(max_length=100)
    answer2 = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question.title


class ListingQuestionair(models.Model):
    question = models.ForeignKey(BasicQuestionair, on_delete=models.CASCADE)
    listing = models.ForeignKey(listing, on_delete=models.CASCADE)
    correct_answer = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.correct_answer
