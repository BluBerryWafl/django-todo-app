from django.shortcuts import render
from base.models import ToDo
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from base.forms import LoginForm, TodoForm


# Create your views here.
def index_view(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            todo = ToDo(text=form.cleaned_data["text"], user=request.user)
            todo.save()
    all_todos = ToDo.objects.all()
    if request.user.is_authenticated:
        all_todos = ToDo.objects.filter(user=request.user)
    form = TodoForm()
    return render(
        request,
        "index.html",
        {
            "name": request.user.username,
            "todos": all_todos,
            "user": request.user,
            "new_todo": form,
        },
    )


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                return HttpResponseRedirect("/login")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form, "user": request.user})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login")


def delete_view(request):
    if request.method == "POST":
        all_todos = ToDo.objects.filter(user=request.user, done=True)
        for todo in all_todos:
            todo.delete()
    return HttpResponseRedirect("/")


def done_view(request):
    if request.method == "POST":
        all_todo = ToDo.objects.filter(
            user=request.user, id__in=request.POST.getlist("done")
        )
        for todo in all_todo:
            todo.done = True
            todo.save()
    return HttpResponseRedirect("/")
