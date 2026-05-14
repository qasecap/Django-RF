from django.db import models
from django.contrib.auth.models import User


class ConfirmationCode(models.Model):
    code = models.CharField(max_length=6)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
