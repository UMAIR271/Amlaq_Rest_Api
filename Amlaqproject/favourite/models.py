from django.db import models
from Amlaq import settings
from listing.models import listing

# Create your models here.
class FavouriteListing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey(listing, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self)-> str:
        return str(self.user) 

