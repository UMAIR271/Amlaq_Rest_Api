from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from loginapp.models import User
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils.translation import gettext_lazy as _


class listing(models.Model):
    Property_Choices = (
        ('A', 'Apartment'),
        ('B', 'Bungalow'),
        ('C', 'Compound'),
        ('D', 'Duplex'),
        ('F', 'Full floor'),
        ('H', 'Half floor'),
        ('L', 'Land'),
        ('P', 'Pent House'),
        ('T', 'Town House'),
        ('V', 'Villa'),
        ('W', 'Whole Building'),
        ('H', 'Hotel apartments'),
        ('U', 'Bulk units'),
    )
    TYPE_CHOIES = (
        ("R", "Residential"),
        ("C", "Commercial"),
    )
    Purpose_Choies = (
        ("S", "Sell"),
        ("R", "Rent"),
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


class notifications(models.Model):
    user_sender = models.ForeignKey(User, related_name='user_sender', on_delete=models.CASCADE, null=True, blank=True)
    user_revoker = models.ForeignKey(User, related_name='user_revoker', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=264, null=True, blank=True, default="unread")
    type_of_notification = models.CharField(max_length=264, null=True, blank=True)


@receiver(post_save, sender=notifications)
def signal_deposit_save(sender, instance, created, **kwargs):
    if created:  # This means it is a new row
        channel_layer = get_channel_layer()
        print(channel_layer, "hello channel layer:::::::")
        async_to_sync(channel_layer.group_send)(
            'test_consumer_group',
            {
                'type': 'infochannel.message',
                'device_id': str(notifications.type_of_notification)
            }
        )


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


class FavouriteListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(listing, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user


class Appointment(models.Model):
    NULL = 'null'
    APPROVED = 'approved'
    DECLINE = 'declined'
    STATUS = (
        (NULL, _('Null')),
        (APPROVED, _('Approved')),
        (DECLINE, _('Decline')),
    )
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="first_user")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="second_user")
    listing = models.ForeignKey(listing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS)

    def __str__(self):
        return self.STATUS


class AvailableSlots(models.Model):
    AVAILABLE = 'available'
    BOOKED = 'booked'
    SLOT_STATUS = (
        (AVAILABLE, _('Available')),
        (BOOKED, _('Booked')),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(listing, on_delete=models.CASCADE)
    time_slots = models.TimeField()
    slot_status = models.CharField(max_length=50, choices=SLOT_STATUS)

    def __str__(self):
        return self.SLOT_STATUS
