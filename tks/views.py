from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from .models import *
from .forms import *

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if request.user.is_authenticated:
        if user.role == "STUDENT" or user.role == "FACULTY":
            return redirect(request, "home_sf.html")
        elif user.role == "TOOL KEEPER":
            return redirect(request, "home_tk.html")

    if request.method == "POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            _username = login_form.cleaned_data.get("username")
            _password = login_form.cleaned_data.get("password")

            user = authenticate(request, username=_username, password=_password)

            if user is not None:
                login(request, user)
                if user.role == "STUDENT" or user.role == "FACULTY":
                    return redirect(request, "home_sf.html")
                elif user.role == "TOOL KEEPER":
                    return redirect(request, "home_tk.html")
            else:
                messages.add_message(request, messages.ERROR, "Username or password incorrect!")
                return redirect('/')
    else:
        login_form = LoginForm()

    context = {"login_form": login_form}
    return render(request, 'index.html', context)

def registration(request):
    pass

def home_sf(request):
    pass

def home_tk(request):
    pass