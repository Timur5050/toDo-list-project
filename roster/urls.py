from django.urls import path

from roster.views import (
    index,
    UserCreateView,
    tasks_list,
    task_create_view,
    task_detail_view,
    user_about,
    #UserUpdateView,
    tag_create,
    tags_list,
    task_completing_view,
)


urlpatterns = [
    path("", index, name="main-page"),
    path("registration/", UserCreateView.as_view(), name="registration"),
    path("users/<str:username>/", user_about, name="user-info"),
    # path("users/<int:pk>/update/", UserUpdateView.as_view(), name="user-update"),
    path("tasks/", tasks_list, name="task-list"),
    path("tasks/create/", task_create_view, name="task-create"),
    path("tasks/<int:pk>/details/", task_detail_view, name="task-details"),
    path("tasks/<int:pk>/completing/", task_completing_view, name="task-completing-change"),
    path("tags/", tags_list, name="tags-list"),
    path("tags/create/", tag_create, name="tag-create"),
]

app_name = "roster"
