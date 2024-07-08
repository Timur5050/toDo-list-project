from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import CreateView
from django.urls import reverse_lazy

from roster.forms import UserForm


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "roster/index.html")


class UserCreateView(CreateView):
    form_class = UserForm
    template_name = "roster/user_form.html"
    success_url = reverse_lazy("roster:main-page")
