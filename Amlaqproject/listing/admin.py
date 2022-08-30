from django.contrib import admin
from .models import listing, notifications, BasicQuestionair, UserQuestionair, ListingQuestionair, FavouriteListing,\
    Appointment, AvailableSlots


# Register your models here.
@admin.register(listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Descriptions', 'Type', 'Purpose_Type', 'Property_Type')


admin.site.register(notifications)
admin.site.register(BasicQuestionair)
admin.site.register(UserQuestionair)
admin.site.register(ListingQuestionair)
admin.site.register(FavouriteListing)
admin.site.register(Appointment)
admin.site.register(AvailableSlots)
