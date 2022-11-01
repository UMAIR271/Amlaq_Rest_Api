from django.db import models
from listing.models import listing
from Amlaq import settings
# Create your models here.



class question(models.Model):
    question_text = models.CharField(max_length=200)
    question_type = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return str(self.question_type)


class ListingQuestion(models.Model):
    question = models.ForeignKey(question, related_name="question",  on_delete=models.CASCADE)
    listing = models.ForeignKey(listing, related_name="listing_question", on_delete=models.CASCADE, null = True)
    expected_Answer =  models.CharField(max_length=300, null = True)






class interestedAnswer(models.Model):

    question = models.ForeignKey(question, related_name="Answer", on_delete=models.CASCADE)
    listing = models.ForeignKey(listing, related_name="listing_anwser", on_delete=models.CASCADE, null = True)
    choice_text = models.CharField(max_length=300)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_id",  on_delete=models.CASCADE, null = True)
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="owner_id",  on_delete=models.CASCADE, null = True)
    save_in_future = models.BooleanField(default=False, null=True)

    def __str__(self):
        return str(self.question)

