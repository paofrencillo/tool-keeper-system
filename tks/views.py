
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.core import serializers
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.db import IntegrityError
from django.conf import settings
from django.core.mail import EmailMessage
from .models import *
from .forms import *


from datetime import datetime
import ast
import pyqrcode
import png
import imghdr
from pyqrcode import QRCode


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        if request.user.role == "STUDENT" or request.user.role == "FACULTY":
            return redirect("home_sf")
        elif request.user.role == "TOOL KEEPER":
            return redirect("transactions_tk")

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
                    return redirect("transactions_tk")
            else:
                messages.add_message(request, messages.ERROR, "Username or password incorrect!")
                return redirect('/')
    else:
        login_form = LoginForm()

    context = {"login_form": login_form}
    return render(request, 'index.html', context)

def userlogout(request):
    logout(request)
    return redirect("index")

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
    if request.user.is_authenticated:
        pass

    tools = Tools.objects.all()
    context = {'tools': tools}

    return render(request, 'sf/home_sf.html', context)

def reservation_sf(request):
    if request.method == "POST":
        ## Get all the tool ids in request.POST
        selected_tools = ast.literal_eval(request.POST.get('selected-tools-all'))

        ## Get the other values in request.POST
        borrow_date = request.POST.get('borrow-date')
        borrow_time = request.POST.get('borrow-time')
        return_date = request.POST.get('return-date')
        return_time = request.POST.get('return-time')

        ## Format date and time from the request.POST
        date_format = '%Y-%m-%d'
        time_format = '%H:%M'
        formatted_borrow_date = datetime.strptime(borrow_date, date_format).date()
        formatted_borrow_time = datetime.strptime(borrow_time, time_format).time()
        formatted_return_date = datetime.strptime(return_date, date_format).date()
        formatted_return_time = datetime.strptime(return_time, time_format).time()

        borrow_datetime = datetime.combine(formatted_borrow_date, formatted_borrow_time).astimezone()
        return_datetime = datetime.combine(formatted_return_date, formatted_return_time).astimezone()

        ## Save new transaction
        borrower = User.objects.get(pk=request.user.pk)

        new_transaction = Transactions.objects.create(
                tupc_id_id=borrower.pk,
                borrow_datetime=borrow_datetime,
                return_datetime=return_datetime,
                status="RESERVED")

        for item in selected_tools:
            TransactionDetails.objects.create(
                    transaction_id_id=new_transaction.pk,
                    tool_id_id=int(item))
        
        #### --- Create message like in the figma design
        #### --- reservation was done
        messages.add_message(request, messages.INFO, "YOWOYW")

        ## Generate QR Code
        # String which represents the QR code
        transaction_code = str(new_transaction.pk)

        # Generate QR code
        qrcode = pyqrcode.create(transaction_code)
        
        # Create and save the png file naming "myqr.png"
        qrcode.png(f'{new_transaction.pk}.png', scale = 6)
        #send email to user
        
        subject = "TKS Transaction Code"
        body = f"""Greetings!\n\n
                This is your QR Code for your transaction with transaction number 
                {transaction_code} in TUP-C Tool Keeper System.\n\n
                This will be used for borrowing and returning the tools you reserved.\n\n
                Please keep in mind to save the QR Code to your device.\n\n
                Thank You!"""
        borrower_email = borrower.email
        email = EmailMessage(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [borrower_email],
            reply_to=[settings.EMAIL_HOST_USER],
            headers={'Message-ID': 'QRCODE'},
        )
        email.attach_file(f'{new_transaction.pk}.png')

        email.send()

        return redirect('home_sf')

    if request.method == "GET":
        ## Get all the tool ids in request.GET
        selected_tools = request.GET.get('selected-tools-all').split(',')
        tools = []

        ## Verify the tool id status if it is available
        ## If not, void reservation
        for item in selected_tools:
            tool = Tools.objects.get(pk=int(item))
            if tool.status == "AVAILABLE":
                tools.append(tool.tool_name)
                ## --- Update tool status to 'RESERVED'
            elif tool.status != "NOT AVAILABLE":
                ### --- Pop up message that the user 
                ### - tool/s selected were not available
                ### --- Then return redirect to the home page
                
                return redirect('home_sf')
    
        context = {'tools': tools,
                'selected_tools_all': selected_tools}

        return render(request, 'sf/reservation_sf.html', context)

def profile_sf(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        #password_form = PasswordChangeForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, f'Account details has been updated!')
            return redirect('profile_sf')
    else:
        form = EditUserForm(instance=request.user)
        #password_form = PasswordChangeForm(user=request.user)
        
    context = {
        'form': form,
        #'password_form': password_form
    }

    return render(request, 'sf/profile_sf.html', context)

def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
    else:
        form = PasswordChangeForm(user=request.user, data=request.POST)
    
        context = {
            'password_change' : password_change
        }
    return render(request, 'sf/password_sf.html', context)

def transactions_sf(request):
    user_transaction = Transactions.objects.filter(tupc_id_id=request.user.pk)
    context = {
        'transactions': user_transaction
    }

    return render(request, 'sf/transactions_sf.html', context)

def transaction_details_sf(request, transaction_id):
    ### --- user authrntication in this block

    if request.method == "POST":
        void_transaction = request.POST.get('void')
    ### --- Try catch errors next time. For the meantime...
        if void_transaction == "Yes, I'm sure":
            transaction = Transactions.objects.get(pk=transaction_id)
            transaction.status = 'VOIDED'
            transaction.save()

            return redirect('transactions_sf')

    transaction_details = Transactions.objects.get(pk=transaction_id)
    tools_borrowed = TransactionDetails.objects.filter(transaction_id_id=transaction_id)
    tools = []
    tool = None

    for t in tools_borrowed:
        tool = Tools.objects.get(pk=t.tool_id_id)
        tools.append(tool)
    
    print(tools)

    context = {
        'transaction_details': transaction_details,
        'tools': tools
    }

    return render(request, 'sf/transaction_details_sf.html', context)

def scanqr_tk(request):
    if request.method == "POST" and request.POST.get('qrcode'):
        qrcode = request.POST.get('qrcode')
        transaction = Transactions.objects.get(pk=int(qrcode))
        transaction_code = transaction.pk

        return redirect("view_transaction_details_tk", transaction_id=transaction_code)

    return render(request, 'tk/scanqr_tk.html')
    
def transactions_tk(request):
    if request.method == "GET" and request.GET.get('filter') == "ALL":
        transactions = Transactions.objects.all().order_by('-pk')

    elif request.method == "GET" and request.GET.get('filter') == "RETURNED":
        transactions = Transactions.objects.filter(status="RETURNED").order_by('-pk')

    elif request.method == "GET" and request.GET.get('filter') == "BORROWED":
        transactions = Transactions.objects.filter(status="BORROWED").order_by('-pk')

    elif request.method == "GET" and request.GET.get('filter') == "RESERVED":
        transactions = Transactions.objects.filter(status="RESERVED").order_by('-pk')

    elif request.method == "GET" and request.GET.get('filter') == "VOIDED":
        transactions = Transactions.objects.filter(status="VOIDED").order_by('-pk')

    else:
        transactions = Transactions.objects.all().order_by('-pk')
        
    context = {'transactions': transactions}

    for i in range(len(transactions)):
        borrow_datetime_str = transactions[i].borrow_datetime.strftime("%b. %d, %Y, %I:%M %p")
        transactions[i].borrow_datetime = transactions[i].borrow_datetime.strptime(borrow_datetime_str, "%b. %d, %Y, %I:%M %p")
        return_datetime_str = transactions[i].return_datetime.strftime("%b. %d, %Y, %I:%M %p") 
        transactions[i].return_datetime = transactions[i].return_datetime.strptime(return_datetime_str, "%b. %d, %Y, %I:%M %p")
        
    return render(request, 'tk/transactions_tk.html', context)

#####################################
# View Transaction Details ToolKeeper
#####################################
def view_transaction_details_tk(request, transaction_id):
    tr_details = Transactions.objects.get(pk=transaction_id)
    borrower = User.objects.get(tupc_id=tr_details.tupc_id_id)
    current_dt_in_sec = timezone.now().timestamp()
    br_dt_in_sec = tr_details.borrow_datetime.timestamp()
    rt_dt_in_sec = tr_details.return_datetime.timestamp()
    is_borrow_dt_late = None
    is_return_dt_late = None
    to_void = None

    if br_dt_in_sec < current_dt_in_sec:
        is_borrow_dt_late = "False"
    if rt_dt_in_sec < current_dt_in_sec:
        is_return_dt_late = "False"

    # Write condition that will void the transaction
    # if the expected datetime if borrow is exceeded 15 min. (900 sec.)
    if (current_dt_in_sec - br_dt_in_sec) >= 900:
        to_void = "Yes"

    # tools_borrowed = ToolsBorrowed.objects.filter(transaction_id_id=transaction_id)
    context = {
        "borrower": borrower,
        "details": tr_details,
        "to_void": to_void,
        "is_borrow_dt_late": is_borrow_dt_late,
        "is_return_dt_late": is_return_dt_late
    }

    return render(request, 'tk/transaction_details_tk.html', context)

def check_datetime_tk(request, transaction_id):
    transaction_details = Transactions.objects.get(id=transaction_id)
    response = {"borrow_datetime": transaction_details.borrow_datetime,
                "return_datetime": transaction_details.return_datetime}
    data = serializers.serialize("json", response)
    print(data)
    return JsonResponse({"datetimes": data})

def borrower_transaction(request):
    # This line of code is for having
    # a database with borrower transaction.
    # For the meantime, this function will
    # return a reserved status html file
    return render(request, 'tk/borrower_transaction/reserved_scanned.html')

def storages_tk(request):
    tools = Tools.objects.all()
    context =  {
        'tools': tools
    }

    return render(request, 'tk/manage_tools/storages_tk.html', context)

def add_tools_tk(request):
    if request.method == "POST":
        try:
            tool_id = request.POST['tool_id']
            tool_name = request.POST['tool_name']
            storage = int(request.POST['storage'])
            layer = int(request.POST['layer'])

            new_tool = Tools.objects.create(
                    tool_id = tool_id,
                    tool_name = tool_name,
                    tool_image = "",
                    storage = storage,
                    layer = layer,
                    status = "AVAILABLE"
            )

            new_tool.save()
            messages.add_message(request, messages.SUCCESS, "TOOL REGISTERED SUCCESSFULLY!")
            return redirect("add_tools_tk")

        except IntegrityError:
            messages.add_message(request, messages.ERROR, "TOOL WAS ALREADY REGISTERED!")
            return redirect("add_tools_tk")

    return render(request, 'tk/manage_tools/add_tools_tk.html')

def edit_tools_tk(request, tool_id):
    return render(request, 'tk/manage_tools/edit_tools_tk.html')