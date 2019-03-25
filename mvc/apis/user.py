from django.contrib.auth.models import User
from rest_framework import viewsets
from mvc.serializer import *


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
