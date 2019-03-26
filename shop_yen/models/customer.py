import uuid
from django.db import models
from mvc.models import *


class Customer(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    CONTACT_TYPE = (
        ('M', 'Mobile'),
        ('P', 'Home phone'),
        ('E', 'Email')
    )

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4())
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    full_name = models.CharField(max_length=100)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, null=True, blank=True)
    contact_type = models.CharField(max_length=2, choices=CONTACT_TYPE)
    contact = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(User, on_delete=models.SET_NULL)
    written_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('full_name', 'contact_type', 'contact')
