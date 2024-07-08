from django.contrib.auth.models import AbstractUser
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50)


class Occupation(models.Model):
    name = models.CharField(max_length=100)


class User(AbstractUser):
    occupation = models.ForeignKey(Occupation, on_delete=models.CASCADE, null=True, blank=True)

    def set_occupation(self, occupation_name):
        occupation, create = Occupation.objects.get_or_create(name=occupation_name)
        self.occupation = occupation
        self.save()
