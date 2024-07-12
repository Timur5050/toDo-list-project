from django.core.paginator import Paginator
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse

from roster.forms import UserForm, TaskForm, TagForm, TaskSearchForm
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


@login_required
def user_about(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(User, username=username)
    context = {
        "user": user
    }
    return render(request, "roster/user_info.html", context=context)


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


@login_required
def tags_list(request: HttpRequest) -> HttpResponse:
    context = {
        "tags_list": Tag.objects.filter(author=request.user),
    }
    return render(request, "roster/tags_list.html", context=context)


@login_required
def tasks_list(request: HttpRequest) -> HttpResponse:
    today = timezone.now().date()
    task_title = request.GET.get("title")

    context = {
        "current_time": today,
        "search_task": TaskSearchForm()
    }

    queryset = Task.objects.filter(user=request.user)
    if task_title:
        queryset = queryset.filter(title__icontains=task_title)

    paginator = Paginator(queryset, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context["task_list"] = page_obj

    return render(request, "roster/task_list.html", context=context)


@login_required
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


@login_required
def task_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    context = {
        "task": Task.objects.get(id=pk)
    }
    return render(request, "roster/task_detail.html", context=context)


@login_required
def task_completing_view(request: HttpRequest, pk=int) -> HttpResponse:
    task = Task.objects.get(id=pk)
    if task.is_completed:
        task.is_completed = False
    else:
        task.is_completed = True
    task.save()
    return redirect(reverse("roster:task-list"))
