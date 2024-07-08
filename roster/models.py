from django.contrib.auth.models import AbstractUser
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="tags"
    )


class Occupation(models.Model):
    name = models.CharField(max_length=100)


class User(AbstractUser):
    occupation = models.ForeignKey(
        Occupation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="users"
    )

    def set_occupation(self, occupation_name):
        occupation, create = Occupation.objects.get_or_create(name=occupation_name)
        self.occupation = occupation
        self.save()


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("HIGH", "high"),
        ("MEDIUM", "medium"),
        ("LOW", "low"),
    )

    title = models.CharField(max_length=30)
    description = models.TextField()
    tag = models.ForeignKey(
        Tag,
        on_delete=models.DO_NOTHING,
        related_name="tasks"
    )
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="LOW"
    )
