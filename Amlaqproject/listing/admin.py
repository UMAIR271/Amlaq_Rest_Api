from django.contrib import admin
from .models import *
# Register your models here.
# @admin.register(listing)
admin.site.register(listing)
admin.site.register(Property_Type)
admin.site.register(Listing_Media)
admin.site.register(compress_image)
admin.site.register(Amenities)
admin.site.register(Listing_Amenities)
admin.site.register(BasicQuestionair)
admin.site.register(UserQuestionair)
admin.site.register(ListingQuestionair)
admin.site.register(FavouriteListing)
admin.site.register(Appointment)
admin.site.register(AvailableSlots)



