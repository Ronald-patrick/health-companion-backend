from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.http import int_to_base36
import uuid

# Create your models here.

def id_gen() -> str:
    return int_to_base36(uuid.uuid4().int)[:6]


class Post(models.Model):
    aid = models.CharField(max_length=6,default='')
    title = models.CharField(max_length=50)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    postid = models.CharField(max_length=6,primary_key=True,default=id_gen)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated']

class AddictionInfo(models.Model):
    aid = models.CharField(max_length=6,primary_key=True,default=id_gen)
    title = models.CharField(max_length=50)
    unit_price = models.DecimalField(decimal_places=2,max_digits=10)
    startDate = models.DateField()
    endDate = models.DateField()

    def __str__(self):
        return self.aid

class UserAddiction(models.Model):
    userid = models.CharField(max_length=6)
    aid = models.CharField(max_length=6)
    def __str__(self):
        return self.userid



class User(AbstractUser):
    id = models.CharField(max_length=6,primary_key=True,default=id_gen)