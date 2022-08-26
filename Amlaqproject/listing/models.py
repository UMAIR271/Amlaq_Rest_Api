from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from Amlaq import settings
# Create your models here.


class listing(models.Model):
    zero = 0
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5 
    six = 6
    saven = 7 
    TYPE_CHOIES = (
        ("Residential" , "Residential"),
        ("Commercial" , "Commercial"),
    )
    Purpose_Choies = (
        ("Sell","Sell"),
        ("Rent","Rent"),
    )
    STATUS_CHOICES = (
    (zero, 'zero'),
    (one, 'one'),
    (two, 'two'),
    (three, 'three'),
    (four, 'three'),


    )
    Purpose_Choies = (
        ("Unfurnised","Unfurnised"),
        ("semi-furnised","semi-furnised"),
        ("furnised","furnised"),
        )
    PROPERTY_TENURE = (
        ("Unfurnised","Unfurnised"),
        ("semi-furnised","semi-furnised"),
        ("furnised","furnised"),
    )
    OCCUPANCY = (
        ("Owner occupied","Owner occupied"),
        ("Investment","Investment"),
        ("Vacant","Vacant"),
        ("Tenanted","Tenanted"),
    )
    PROJECT_STATUS = (
        ("Off plane","Off plane"),
        ("completed","completed"),
    )
    RENOVATION_TYPE = (
        ("Fully upgraded","Fully upgraded"),
        ("Partially upgraded","Partially upgraded"),
    )
    FINANCIAL_STATUS = (
        ("Mortgaged","Mortgaged"),
        ("Cash","Cash"),
    )

    user_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    Title = models.CharField(max_length=50)
    Descriptions = models.CharField(max_length=300)
    Type = models.CharField(max_length=11, choices=TYPE_CHOIES)
    Purpose_Type = models.CharField(max_length=13, choices=Purpose_Choies)
    Property_Type = models.ForeignKey("Property_Type", on_delete=models.CASCADE)
    Bedrooms = models.IntegerField(max_length=1, choices=STATUS_CHOICES)
    Batrooms = models.IntegerField(max_length=1, choices=STATUS_CHOICES)
    Furnishing_type = models.CharField(max_length=11, choices=TYPE_CHOIES)
    Property_Tenure = models.CharField(max_length=13, choices=PROPERTY_TENURE)
    size = models.CharField(max_length=300)
    Build_up_Area = models.CharField(max_length=300)
    parking_number = models.CharField(max_length=300)
    Property_Developer = models.CharField(max_length=300)
    Build_year = models.CharField(max_length=300)
    Building_Floor = models.CharField(max_length=300)
    Floor_number = models.CharField(max_length=300)
    Dewa_number =  models.CharField(max_length=300)
    Occupancy = models.CharField(max_length=14, choices=OCCUPANCY)
    Project_status = models.CharField(max_length=9, choices=PROJECT_STATUS)
    Renovation_type = models.CharField(max_length=18, choices=RENOVATION_TYPE)
    Layout_type = models.CharField(max_length=300)
    property_pricing  = models.CharField(max_length=300)
    Service_charge  = models.CharField(max_length=300)
    financial_status = models.CharField(max_length=9, choices=FINANCIAL_STATUS)
    Cheques = models.IntegerField(max_length=1, choices=STATUS_CHOICES)
    property_location = models.CharField(max_length=300)
    street_Address = models.CharField(max_length=300)
    project_name = models.CharField(max_length=300)


class Property_Type(models.Model):
    Property_Choices = (
        ('A' , 'Apartment'),
        ('B' , 'Bungalow'),
        ('C' , 'Compound'),
        ('D' , 'Duplex'),
        ('F' , 'Full floor'),
        ('H' , 'Half floor'),
        ('L' , 'Land'),
        ('P' , 'Pent House'),
        ('T' , 'Town House'),
        ('V' , 'Villa'),
        ('W' , 'Whole Building'),
        ('H' , 'Hotel apartments'),
        ('U' , 'Bulk units'),
    )
    Property_name = models.CharField(max_length=1, choices=Property_Choices)





class Listing_Media(models.Model):
    listing = models.ForeignKey(listing, related_name="list", on_delete=models.CASCADE )
    images_path = models.ImageField(upload_to ='uploads/')

    def __str__(self) -> str:
        return str({'images':self.images_path})



class Amenities(models.Model):
    AMENITIES = (
        ("D","Dishwasher"),
        ("F","Fireplace"),
        ("S","Swimming pool"),
    )
    listing = models.ForeignKey(listing, related_name="Amenities", on_delete=models.CASCADE )
    Amenities_Name = models.CharField(max_length=20, choices=AMENITIES )
    Cration_Time = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return str({'Amenities':self.Amenities_Name})


class Listing_Amenities(models.Model):
    listing = models.ForeignKey(listing, on_delete=models.CASCADE)
    Amenities_ID = models.ForeignKey("Amenities", on_delete=models.CASCADE)
    Cration_Time = models.DateTimeField(auto_now_add=True)


