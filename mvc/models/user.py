from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    timezone = models.CharField(max_length=50, null=True, blank=True)

    @property
    def name(self):
        name = '{} {}'.format(self.first_name, self.last_name).strip()
        if not name:
            name = 'User #{}'.format(self.pk)
        return name

    def __str__(self):
        return self.name
