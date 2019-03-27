import uuid
from django.db import models
from enum import Enum
from mvc.models import *


# Gender Choice
class GenderChoice(Enum):
    M = 'Male'
    F = 'Female'


# Gender Choice
class ContactChoice(Enum):
    M = 'Mobile'
    P = 'Home phone'
    E = 'Email'


class Customer(models.Model):
    __GENDER_CHOICES = [(tag.name, tag.value) for tag in GenderChoice]
    __CONTACT_CHOICES = [(tag.name, tag.value) for tag in ContactChoice]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    full_name = models.CharField(max_length=100)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=2, choices=__GENDER_CHOICES, null=True, blank=True)
    contact_type = models.CharField(max_length=2, choices=__CONTACT_CHOICES)
    contact = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_customer')
    created_date = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wrote_customer')
    modified_date = models.DateTimeField(auto_now=True)

    @property
    def name(self):
        name = '{} {}: {}'.format(self.first_name, self.last_name, self.contact).strip()
        if not name:
            name = 'User #{}'.format(self.pk)
        return name

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('full_name', 'contact_type', 'contact')
