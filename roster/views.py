from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy

from roster.forms import UserForm, TaskForm
from roster.models import Task


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "roster/index.html")


class UserCreateView(CreateView):
    form_class = UserForm
    template_name = "roster/user_form.html"
    success_url = reverse_lazy("roster:main-page")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object

        login(self.request, user)

        return response


class TaskListView(ListView):
    model = Task
    fields = "__all__"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("roster:task-list")
