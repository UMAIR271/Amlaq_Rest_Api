from django.contrib import admin
from .models import listing
# Register your models here.
@admin.register(listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Descriptions','Type','Purpose_Type','Property_Type')
