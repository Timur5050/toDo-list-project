from django.urls import path

from roster.views import (
    index,
    UserCreateView,
    TaskListView,
    TaskCreateView
)


urlpatterns = [
    path("", index, name="main-page"),
    path("registration/", UserCreateView.as_view(), name="registration"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
]

app_name = "roster"
