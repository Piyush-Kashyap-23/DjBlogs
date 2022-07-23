from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("post/<str:pk>/", views.getPost, name="post_detail") ,
    path("post/<str:pk>/delete/", views.deletePost, name="post_delete"),
    path("new_post/", views.createPost, name="post_create"),
    path("post/<str:pk>/edit/", views.updatePost, name="post_update"),
    path("login/", views.loginUser, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("signup/", views.registerUser, name="register"),
    path("my_account/", views.myAccount, name="my_account")
]
