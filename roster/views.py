from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy

from roster.forms import UserForm, TaskForm, TagForm
from roster.models import Task, User, Tag


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


def user_about(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(User, username=username)
    context = {
        "user": user
    }
    return render(request, "roster/user_info.html", context=context)


# class UserUpdateView(LoginRequiredMixin, UpdateView):
#     model = User
#     form_class = UserForm
#     template_name = "roster/user_form.html"
#     #success_url = reverse_lazy("roster:user-info", )
@login_required
def tag_create(request: HttpRequest) -> HttpResponse:
    context = {
        "form": TagForm
    }
    if request.method == "GET":
        return render(request, "roster/tag_form.html", context=context)
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.author = request.user
            tag.save()
            return redirect(reverse_lazy("roster:tags-list"))


def tags_list(request: HttpRequest) -> HttpResponse:
    context = {
        "tags_list": Tag.objects.filter(author=request.user)
    }
    return render(request, "roster/tags_list.html", context=context)


def tasks_list(request: HttpRequest) -> HttpResponse:
    context = {
        "task_list": Task.objects.filter(user=request.user)
    }
    return render(request, "roster/task_list.html", context=context)


def task_create_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        context = {
            "form": TaskForm(current_user=request.user)
        }
        return render(request, "roster/task_form.html", context=context)
    if request.method == "POST":
        form = TaskForm(request.POST, current_user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect(reverse_lazy("roster:task-list"))
