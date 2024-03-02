from django.db import models
from email.policy import default

# Create your models here.
class user(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50, default='')
    password = models.CharField(max_length=50)
    status = models.BooleanField(default='1')

    def __str__(self):
        return self.name


class resultHistory(models.Model):
    user_id = models.CharField(max_length=100)
    text = models.CharField(max_length=50, default='')
    result = models.CharField(max_length=50)
    date = models.DateField(default='1')
    language = models.CharField(max_length=50, default='')

    def __str__(self):
        return str(self.date) + " : " + str(self.user_id)+ " : " + str(self.result)
