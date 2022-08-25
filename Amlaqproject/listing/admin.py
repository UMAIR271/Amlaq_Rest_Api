from django.contrib import admin
from .models import listing, notifications


# Register your models here.
@admin.register(listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Descriptions', 'Type', 'Purpose_Type', 'Property_Type')


admin.site.register(notifications)
