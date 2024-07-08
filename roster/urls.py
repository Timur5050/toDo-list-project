from django.urls import path

from roster.views import index, UserCreateView


urlpatterns = [
    path("", index, name="main-page"),
    path("registration/", UserCreateView.as_view(), name="registration")
]

app_name = "roster"
