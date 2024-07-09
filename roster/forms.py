from django import forms
from django.contrib.auth.forms import UserCreationForm

from roster.models import User


class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "occupation"
        )