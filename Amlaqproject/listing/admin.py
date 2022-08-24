from django.contrib import admin
from .models import *
# Register your models here.
# @admin.register(listing)
admin.site.register(listing)
admin.site.register(Property_Type)
admin.site.register(Listing_Media)
admin.site.register(Amenities)
admin.site.register(Listing_Amenities)



