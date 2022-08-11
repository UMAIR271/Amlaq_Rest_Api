from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class listing(models.Model):
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
    TYPE_CHOIES = (
        ("R" , "Residential"),
        ("C" , "Commercial"),
    )
    Purpose_Choies = (
        ("S","Sell"),
        ("R","Rent"),
    )
    LOW = 0
    NORMAL = 1
    HIGH = 2
    STATUS_CHOICES = (
    (LOW, 'Low'),
    (NORMAL, 'Normal'),
    (HIGH, 'High'),
)
    Title = models.CharField(max_length=50)
    Descriptions = models.CharField(max_length=300)
    Type = models.CharField(max_length=1, choices=TYPE_CHOIES)
    Purpose_Type = models.CharField(max_length=1, choices=Purpose_Choies)
    Property_Type = models.CharField(max_length=1, choices=Property_Choices)
    # Bedrooms = models.IntegerField(max_length=1, choices=TYPE_CHOIES)
    # Furnishing_type = models.CharField(max_length=1, choices=TYPE_CHOIES)

