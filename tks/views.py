from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from .models import *
from .forms import *
from django.http import JsonResponse
from datetime import datetime


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        if request.user.role == "STUDENT" or request.user.role == "FACULTY":
            return redirect("home_sf")
        elif request.user.role == "TOOL KEEPER":
            return redirect("home_tk")

    if request.method == "POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            _username = login_form.cleaned_data.get("username")
            _password = login_form.cleaned_data.get("password")

            user = authenticate(request, username=_username, password=_password)

            if user is not None:
                login(request, user)
                if user.role == "STUDENT" or user.role == "FACULTY":
                    return redirect("home_sf")
                elif user.role == "TOOL KEEPER":
                    return redirect("home_tk")
            else:
                messages.add_message(request, messages.ERROR, "Username or password incorrect!")
                return redirect('/')
    else:
        login_form = LoginForm()

    context = {"login_form": login_form}
    return render(request, 'index.html', context)

def registration_role(request):
    return render(request, "register_as.html")

def registration_student(request):
    if request.user.is_authenticated:
        if request.user.role == "STUDENT" or request.user.role == "FACULTY":
            return redirect(request, "home_sf.html")
        elif request.user.role == "TOOL KEEPER":
            return redirect(request, "home_tk.html")
    
    if request.method == "POST":
        registration_form = StudentRegistrationForm(request.POST)

        if registration_form.is_valid():
            registration_form.save()
            messages.add_message(request, messages.SUCCESS, "Account created successfully!")
            return redirect('/')
        else:
            pass   
    else:
        registration_form = StudentRegistrationForm()

    context = {"registration_form": registration_form}
    return render(request, 'register_student.html', context)
    
def registration_faculty(request):
    if request.user.is_authenticated:
        if request.user.role == "FACULTY" or request.user.role == "STUDENT":
            return redirect(request, "sf/home_sf.html")
        elif request.user.role == "TOOL KEEPER":
            return redirect(request, "tk/home_tk.html")
    
    if request.method == "POST":
        registration_form = FacultyRegistrationForm(request.POST)

        if registration_form.is_valid():
            new_user = registration_form.save(commit=False)
            new_user.year_course = None
            new_user.save()
            messages.add_message(request, messages.SUCCESS, "Account created successfully!")
            return redirect('/')
        else:
            pass
    else:
        registration_form = FacultyRegistrationForm()

    context = {"registration_form": registration_form}
    return render(request, 'register_faculty.html', context)

def registration_toolkeeper(request):
    if request.user.is_authenticated:
        if request.user.role == "TOOL KEEPER":
            return redirect(request, "tk/home_tk.html")
        elif request.user.role == "FACULTY" or request.user.role == "STUDENT":
            return redirect(request, "sf/home_sf.html")
    
    if request.method == "POST":
        registration_form = ToolKeeperRegistrationForm(request.POST)

        if registration_form.is_valid():
            new_user = registration_form.save(commit=False)
            new_user.year_course = None
            new_user.save()
            messages.add_message(request, messages.SUCCESS, "Account created successfully!")
            return redirect('/')
        else:
            # Put something here when form is invalid...
            pass
    else:
        registration_form = ToolKeeperRegistrationForm()

    context = {"registration_form": registration_form}
    return render(request, 'register_toolkeeper.html', context)

def home_sf(request):
    return render(request, 'sf/home_sf.html')

def reservation_sf(request):
    # if request.user.is_authenticated:
    #     if request.user.role == "TOOL KEEPER":
    #         return redirect("transactions_tk")
    #     elif request.user.role == "FACULTY" or request.user.role == "STUDENT":
    #         return redirect("home_sf")

    if request.method == "POST":
        fullname = request.POST.get('fullname')
        role = request.POST.get('role')
        tupc_id = request.POST.get('tupc-id')
        borrow_date = request.POST.get('borrow-date')
        borrow_time = request.POST.get('borrow-time')
        return_date = request.POST.get('return-date')
        return_time = request.POST.get('return-time')
        'Paolo Frencillo BET-COET-NS-4B 190472 2022-10-23 18:57 2022-10-29 18:03'

        date_format = '%Y-%m-%d'
        time_format = '%H:%M'
        borrow_date = datetime.strptime(borrow_date, date_format).date()
        borrow_time = datetime.strptime(borrow_time, time_format).time()
        return_date = datetime.strptime(return_date, date_format).date()
        return_time = datetime.strptime(return_time, time_format).time()

        borrow_datetime = datetime.combine(borrow_date, borrow_time).astimezone()
        return_datetime = datetime.combine(return_date, return_time).astimezone()


        borrower = User.objects.get(id=request.user.id)

        Transactions.objects.create(
                borrower_id=borrower,
                fullname=fullname,
                borrow_datetime=borrow_datetime,
                return_datetime=return_datetime,
                status="RESERVED")

        # Create object on tools borrowed
        # ...
        # Then return render into the home page
    return render(request, 'sf/reservation_sf.html')

def profile_sf(request):
    return render(request, 'sf/profile_sf.html')

def transactions_sf(request):
    return render(request, 'sf/transactions_sf.html')

def view_transactions(request):
    return render(request, 'sf/view_transactions.html')

def scanqr_tk(request):
    return render(request, 'tk/scanqr_tk.html')
    
def transactions_tk(request):
    transactions = Transactions.objects.all().order_by('-id')
    context = {'transactions': transactions}
    return render(request, 'tk/transactions_tk.html', context)

def borrower_transaction(request):
    # This line of code is for having
    # a database with borrower transaction.
    # For the meantime, this function will
    # return a reserved status html file
    return render(request, 'tk/borrower_transaction/reserved_scanned.html')

def storages_tk(request):
    return render(request, 'tk/manage_tools/storages_tk.html')

def add_tools_tk(request):
    return render(request, 'tk/manage_tools/add_tools_tk.html')

def edit_tools_tk(request):
    return render(request, 'tk/manage_tools/edit_tools_tk.html')