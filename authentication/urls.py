from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.my_login, name="my_login"),
    path("register", views.register, name="register"),
    path("signout", views.signout, name="signout"),
    path("table", views.table, name="table"),
    path("issue/add", views.add_issue, name="add"),
    path("update_issue_status/", views.update_issue_status, name='update_issue_status'),
    path("issue/<int:id>", views.update_issue, name="update_issue")
]
