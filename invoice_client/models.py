from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Client(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    date = models.DateTimeField(default=now)
    bill_date = models.DateTimeField(default=now)

    class Meta:
        ordering = ('user__first_name', )


class Work(models.Model):

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    fee = models.FloatField()
    date = models.DateTimeField(default=now)

    class Meta:
        ordering = ('date', )
