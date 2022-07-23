from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Post, Comment
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
def search_posts(request):
    post_search = ""
    if request.GET.get("search"):
        post_search = request.GET.get('search')
    posts = Post.objects.filter(Q(title__icontains=post_search) | Q(body__icontains=post_search))
    return posts

def index(request):
    posts = search_posts(request)
    context = { "posts": posts }
    return render(request, "index.html", context)

# Auth

def registerUser(request):
    if request.user.is_authenticated:
        return redirect("home")

    context = {}
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()

            login(request, user)
            return redirect("home")

    return render(request, "register.html", context)

def loginUser(request):
    if request.user.is_authenticated:
        return redirect("home")
    context = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            context = {"message": "*Username or password is incorrect"}

    return render(request, "login.html", context)

@login_required(login_url="login")
def logoutUser(request):
    logout(request)
    return redirect("home")

@login_required(login_url="login")
def myAccount(request):
    user = request.user
    user_posts = Post.objects.filter(author=user)
    context = {"posts":user_posts}
    context["capitalize_username"] = request.user.username.capitalize()
    return render(request, "my_account.html", context)

# Posts CRUD
def getPost(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == "POST":
        comment = request.POST.get("comment")
        Comment.objects.create(
            post = post,
            author = request.user,
            comment = comment
        )
    return render(request, "post_detail.html", { "post":post })

@login_required(login_url="login")
def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    if request.user == post.author:
        post.delete()
    else:
        return HttpResponse("403 FORBIDDEN")
    return redirect("home")

@login_required(login_url="login")
def createPost(request):
    context = {}
    if request.method == "POST":
        try:
            Post.objects.create(
                title = request.POST.get("title"),
                body = request.POST.get("description"),
                author = request.user
            )
            return redirect("home")
        except:
            context["message"] = "*Invalid details"
    return render(request, "new_post.html", context)

@login_required(login_url="login")
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    if request.user == post.author:
        context = {"post":post}
        if request.method == "POST":
            post.title = request.POST.get("title")
            post.body = request.POST.get("description")
            post.save()
            return redirect("home")
            
        return render(request, "post_update.html", context)
    else:
        return HttpResponse("403 FORBIDDEN")