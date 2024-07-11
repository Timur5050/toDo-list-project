from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import DateInput

from roster.models import User, Task, Tag


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "occupation"
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class TaskForm(forms.ModelForm):
    deadline = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

        self.fields['tag'].queryset = Tag.objects.filter(author_id=self.current_user.id)

    tag = forms.ModelChoiceField(
        required=False,
        queryset=Tag.objects.none()
    )

    class Meta:
        model = Task
        fields = ("title", "description", "tag", "deadline", "priority", )


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("name", )
