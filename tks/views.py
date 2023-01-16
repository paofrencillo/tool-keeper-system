
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.db import IntegrityError
from django.db.models import Q
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.base import ContentFile
from django.utils.http import urlsafe_base64_encode
from django.utils import timezone
from django.http import HttpResponse
from .models import *
from .forms import *
from datetime import datetime
import base64
import ast
import requests
import qrcode
import os


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
            new_user = registration_form
            new_user.save()
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


@login_required(login_url='index')
def home_sf(request):
    tools = Tools.objects.filter(status="AVAILABLE").exclude(is_removed=True).order_by("tool_name").values_list('tool_name', flat=True).distinct()
    tool_quantity = ToolQuantity.objects.all().order_by("tool_name")

    group_by_value = {}

    for value in tools:
        group_by_value[value] = Tools.objects.filter(tool_name=value)
    
    i = 0
    for key, value in list(group_by_value.items()):
        if tool_quantity[i].tool_name == key:
            if tool_quantity[i].quantity == 0:
                del group_by_value[key]
        i += 1

    if request.user.is_authenticated:
        if request.user.role == "TOOL KEEPER":
            return redirect("transactions_tk")
    
    if request.user.has_ongoing_transaction == True:
        messages.add_message(request,
                messages.WARNING,
                "You have ongoing transaction. Void your reservation or return the tool/s you borrowed.",
                extra_tags="has_ongoing_transaction")
        return render(request, 'sf/home_sf.html')
    
    if tools.count() == 0:
        messages.add_message(request,
                messages.INFO,
                "There are no available tools for this moment. Try again later.",
                extra_tags="no_tools")
        return render(request, 'sf/home_sf.html')

    context = {"tools": group_by_value}
    return render(request, 'sf/home_sf.html', context)


@login_required(login_url='index')
def reservation_sf(request):
    if request.user.is_authenticated:
        if request.user.role == "TOOL KEEPER":
            return redirect("transactions_tk")

    if request.method == "POST":
        if request.POST.get('submit_option') == "OK":
            ## Get all the tool ids in request.POST
            selected_tools = ast.literal_eval(request.POST.get('selected-tools-all'))
            not_available_tools = []

            for item in selected_tools:
                if ToolQuantity.objects.get(tool_name=item).quantity == 0:
                    not_available_tools.append(item)

            if not_available_tools != []:
                messages.add_message(request,
                            messages.ERROR,
                            f"{' ,'.join(not_available_tools)}",
                            extra_tags="tools_unavailable")
                return redirect("home_sf")
                
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
            borrower.has_ongoing_transaction = True
            borrower.save()

            new_transaction = Transactions.objects.create(
                tupc_id_id=borrower.tupc_id,
                entry_datetime=datetime.now(tz=timezone.utc),
                expected_borrow=borrow_datetime,
                expected_return=return_datetime,
                status="RESERVED")

            for item in selected_tools:
                tool = ToolQuantity.objects.get(tool_name=item)
                tool.quantity -= 1
                tool.save()

                ReservedTools.objects.create(
                   transaction_id = new_transaction,
                   tool_name = item 
                )

            # Generate QR code
            transaction_code = str(new_transaction.pk)

            # Creating an instance of qrcode
            qr = qrcode.QRCode(
                    version=1,
                    box_size=10,
                    border=5)
            qr.add_data(transaction_code)
            qr.make(fit=True)
            qrcode_img = qr.make_image(fill='black', back_color='white')
            qrcode_img_file = f'{borrower.last_name+transaction_code[:2]+transaction_code[5:10]+transaction_code[-5:]}.png'
            qrcode_img.save(qrcode_img_file)
        
            # Send email to user
            subject = "TKS Transaction Code"
            body = f"Greetings!\n\
                    This is your QR Code for your transaction in TUP-C Tool Keeper System.\n\
                    This will be used for borrowing and returning the tools you reserved.\n\
                    Please keep in mind to save the QR Code to your device.\n\n\
                    Thank You!"
            sender = f"TUP-C Tool Keeper System <from {settings.EMAIL_HOST_USER}>"
            borrower_email = borrower.email

            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=sender,
                to=[borrower_email],
                headers={'Message-ID': 'QRCODE'},
            )

            email.attach_file(qrcode_img_file)
            email.send()

            # Delete generated qrcode in the root directory
            os.remove(qrcode_img_file)

            return redirect('home_sf')

        elif request.POST.get('submit_option') == "YES":
            return redirect('home_sf')

    if request.method == "GET":
        selected_tools = request.GET.get('selected-tools-all').split(',')
        not_available_tools = []

        for item in selected_tools:
            if ToolQuantity.objects.get(tool_name=item).quantity == 0:
                not_available_tools.append(item)
                print(not_available_tools)

        if not_available_tools != []:
            messages.add_message(request,
                        messages.ERROR,
                        f"{' ,'.join(not_available_tools)}",
                        extra_tags="tools_unavailable")
            return redirect("home_sf")
            
        context = {'selected_tools_all': selected_tools}
        return render(request, "sf/reservation_sf.html", context)

@login_required(login_url='index')
def transactions_sf(request):
    if request.user.is_authenticated:
        if request.user.role == "TOOL KEEPER":
            return redirect("transactions_tk")
        
    transactions = Transactions.objects.filter(tupc_id_id=request.user.tupc_id).order_by('-entry_datetime')
    context = {
        'transactions': transactions
    }

    return render(request, 'sf/transactions_sf.html', context)

@login_required(login_url='index')
def transaction_details_sf(request, transaction_id):
    transaction = Transactions.objects.get(pk=transaction_id)
    tools = Tools.objects.filter(current_transaction=transaction_id)
    borrower = User.objects.get(pk=request.user.pk)
    finished = FinishedTransactions.objects.filter(transaction_id=transaction.pk)
    reserved_tools = ReservedTools.objects.filter(transaction_id=transaction.pk)
    voided = VoidedTransactions.objects.filter(transaction_id=transaction.pk)

    if request.user.is_authenticated:
        transaction = Transactions.objects.get(pk=transaction_id)
        get_borrower = transaction.tupc_id_id
        if request.user.role == "TOOL KEEPER":
            return redirect("transactions_tk")
        if get_borrower != request.user.tupc_id:
            return redirect("home_sf")

    if request.method == "POST":
        transaction = Transactions.objects.get(pk=transaction_id)
        reserved_tools = ReservedTools.objects.filter(transaction_id=transaction_id)
        borrower = User.objects.get(tupc_id=transaction.tupc_id_id)

        for tool in reserved_tools:
            update_tool_quantity = ToolQuantity.objects.get(tool_name=tool.tool_name)
            update_tool_quantity.quantity += 1
            update_tool_quantity.save()

            VoidedTransactions.objects.create(
                transaction_id = transaction,
                tool_name = tool.tool_name,
            )

        transaction.status = "VOIDED"
        transaction.voided_by = request.user
        transaction.voided_on = datetime.now(tz=timezone.utc)
        transaction.save()

        borrower.has_ongoing_transaction = False
        borrower.save()

        reserved_tools.delete()

        return redirect('transactions_sf')

    context = {
        'transaction': transaction,
        'tools': tools,
        'finished': finished,
        'reserved_tools': reserved_tools,
        'voided': voided
    }

    return render(request, 'sf/transaction_details_sf.html', context)

@login_required(login_url='index')
def profile_sf(request):
    if request.user.is_authenticated:
        if request.user.role == "TOOL KEEPER":
            return redirect("transactions_tk")

    if request.method == 'POST' and request.FILES.get('imageUpload') == None:
        form = EditUserForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Account details updated successfully!", extra_tags="details_change_success")
            return redirect('profile_sf')
    
    if request.method == "POST" and request.FILES.get('imageUpload'):
        img = request.FILES.get('imageUpload')
        _user = User.objects.get(pk=request.user.pk)
        _user.user_img = img
        _user.save()
        messages.add_message(request, messages.SUCCESS, "Profile picture updated successfully!", extra_tags="img_change_success")

        return redirect('profile_sf')
    
    form = EditUserForm(instance=request.user)
        
    context = {
        'form': form,
    }

    return render(request, 'sf/profile_sf.html', context)

@login_required(login_url='index')
def change_password_sf(request):
    if request.user.is_authenticated:
        if request.user.role == "TOOL KEEPER":
            return redirect("transactions_tk")

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.add_message(request, messages.SUCCESS, "Password changed successfully!", extra_tags="pass_change_success")
            return redirect("profile_sf")
    
    else:
        form = PasswordChangeForm(user=request.user)
    
    context = {
        'form': form
    }
    
    return render(request, 'sf/change_password_sf.html', context)

@login_required(login_url='index')
def scanqr_tk(request):
    if request.user.is_authenticated:
        if request.user.role == "STUDENT" or request.user.role == "FACULTY":
            return redirect("home_sf")

    if request.method == "POST" and request.POST.get('qrcode'):
        qrcode = request.POST.get('qrcode')
        transaction = Transactions.objects.get(pk=qrcode)
        transaction_code = transaction.pk

        return redirect("transaction_details_tk", transaction_id=transaction_code)

    return render(request, 'tk/scanqr_tk.html')



@login_required(login_url='index') 
def transactions_tk(request):
    if request.user.is_authenticated:
        if request.user.role == "STUDENT" or request.user.role == "FACULTY":
            return redirect("home_sf")

    transactions = Transactions.objects.all().order_by('-entry_datetime') 
    context = {'transactions': transactions}
        
    return render(request, 'tk/transactions_tk.html', context)

#####################################
# View Transaction Details ToolKeeper
#####################################
def borrow_tools_tk(request, transaction_id):
    if request.method == "POST":
        try:
            rpi_ip = RpiIP.objects.get(pk=1)
            r = requests.get(f"http://{rpi_ip.ip_address}/checkRPI")
            

        except requests.Timeout:
            return HttpResponseNotFound('<h1>Make Sure that the Raspberry Pi is ON and storages are connected.</h1>')

        transaction = Transactions.objects.get(pk=transaction_id)
        reserved_tools = ReservedTools.objects.filter(transaction_id=transaction_id)
        
        for tool in reserved_tools:
            tool_id = request.POST.get(f"{tool.tool_name}_input")
            tool_to_borrow = Tools.objects.get(pk=tool_id)
            tool_to_borrow.current_transaction = transaction
            tool_to_borrow.current_user = transaction.tupc_id
            tool_to_borrow.status = "BORROWED"
            tool_to_borrow.save()

            transaction.actual_borrowed = datetime.now(tz=timezone.utc)
            transaction.status = "BORROWED"
            transaction.save()

        reserved_tools.delete()

        messages.add_message(request, messages.SUCCESS, "Transaction complete. Tools are now being borrowed.", extra_tags="borrow_success")
        return redirect('transaction_details_tk', transaction_id)

    return HttpResponseNotFound("<h1>Page not found</h1>")

def return_tools_tk(request, transaction_id):
    if request.method == "POST":
        try:
            rpi_ip = RpiIP.objects.get(pk=1)
            r = requests.get(f"http://{rpi_ip.ip_address}/checkRPI")
            

        except requests.Timeout:
            return HttpResponseNotFound('<h1>Make Sure that the Raspberry Pi is ON and storages are connected.</h1>')

        transaction = Transactions.objects.get(pk=transaction_id)
        tools_borrowed = Tools.objects.filter(current_transaction_id=transaction.pk)
        borrower = User.objects.get(tupc_id=transaction.tupc_id_id)
        remarks = []

        for tool in tools_borrowed:
            r = request.POST.get(f'add_remarks{tool.pk}')
            if r == "r1":
                tool.status = "RETURNED WITH DAMAGE"
                remarks.append("RETURNED WITH DAMAGE")
                tool.current_transaction = None
                tool.current_user = None
                tool.status = "DAMAGED"
                tool.save()

                update_tool_quantity = ToolQuantity.objects.get(tool_name=tool.tool_name)
                update_tool_quantity.quantity += 1
                update_tool_quantity.save()

                FinishedTransactions.objects.create(
                    transaction_id = transaction,
                    tool_borrowed = tool,
                    tool_status = "RETURNED WITH DAMAGE"
                )

            elif r == "r2":
                tool.status = "MISSING"    
                remarks.append("MISSING")
                tool.current_transaction = None
                tool.current_user = None   
                tool.status = "MISSING"        
                tool.save()
                
                FinishedTransactions.objects.create(
                    transaction_id = transaction,
                    tool_borrowed = tool,
                    tool_status = "MISSING"
                )

            elif r != "r1" and r != "r2":
                tool.status = "AVAILABLE"  
                tool.current_transaction = None
                tool.current_user = None
                tool.save()

                update_tool_quantity = ToolQuantity.objects.get(tool_name=tool.tool_name)
                update_tool_quantity.quantity += 1
                update_tool_quantity.save()

                FinishedTransactions.objects.create(
                    transaction_id = transaction,
                    tool_borrowed= tool,
                    tool_status = "RETURNED"
                )
            
            borrower.has_ongoing_transaction = False
            borrower.save()

        if remarks == []:
            transaction.status = "RETURNED"

        if "RETURNED WITH DAMAGE" in remarks and "MISSING" in remarks:
            transaction.status = "RETURNED WITH DAMAGE AND MISSING"
        
        elif "RETURNED WITH DAMAGE" in remarks:
            transaction.status = "RETURNED WITH DAMAGE"

        elif "MISSING" in remarks:
            transaction.status = "RETURNED WITH MISSING"

        transaction.actual_returned = datetime.now(tz=timezone.utc)
        transaction.save()

        return redirect ("transaction_details_tk", transaction_id)
    
    return HttpResponseNotFound("<h1>Page not found</h1>")

def void_tools_tk(request, transaction_id):
    if request.method == "POST":
        transaction = Transactions.objects.get(pk=transaction_id)
        reserved_tools = ReservedTools.objects.filter(transaction_id=transaction_id)
        borrower = User.objects.get(tupc_id=transaction.tupc_id_id)

        for tool in reserved_tools:
            update_tool_quantity = ToolQuantity.objects.get(tool_name=tool.tool_name)
            update_tool_quantity.quantity += 1
            update_tool_quantity.save()

            VoidedTransactions.objects.create(
                transaction_id = transaction,
                tool_name = tool.tool_name,
            )
        transaction.status = "VOIDED"
        transaction.voided_by = request.user
        transaction.voided_on = datetime.now(tz=timezone.utc)
        transaction.save()

        borrower.has_ongoing_transaction = False
        borrower.save()

        reserved_tools.delete()

        return redirect('transaction_details_tk', transaction_id)

    return HttpResponseNotFound("<h1>Page not found</h1>")

@login_required(login_url='index')
def transaction_details_tk(request, transaction_id):
    if request.user.is_authenticated:
        if request.user.role == "STUDENT" or request.user.role == "FACULTY":
            return redirect("home_sf")
            
    if request.method == "GET":
        transaction = Transactions.objects.get(pk=transaction_id)
        borrower = User.objects.get(tupc_id=transaction.tupc_id_id)

        if transaction.status == "RESERVED":
            reserved_tools = ReservedTools.objects.filter(transaction_id=transaction_id).order_by("tool_name")

            group_by_tool_name = {}
            from django.db.models import Count

            for value in reserved_tools:
                group_by_tool_name[value.tool_name] = list(Tools.objects.filter(tool_name=value.tool_name).filter(status="AVAILABLE").values('storage', 'layer').annotate(count=Count('tool_name')).distinct())
            
            print(group_by_tool_name)
            context = {
                "borrower": borrower,
                "transaction": transaction,
                "reserved_tools": group_by_tool_name
            }

            return render(request, "tk/transactions/reserved.html", context)
        
        elif transaction.status == "BORROWED":
            tools_borrowed = Tools.objects.filter(current_transaction_id=transaction.pk)
            storages = []

            for tool in tools_borrowed:
                storages.append(tool.storage)
                storages = list(dict.fromkeys(storages))

            storages.sort()
    
            context = {
                "borrower": borrower,
                "transaction": transaction,
                "tools_borrowed": tools_borrowed,
                "storages": storages
            }
            
            return render(request, "tk/transactions/borrowed.html", context)

        elif transaction.status == "RETURNED" or transaction.status == "RETURNED WITH DAMAGE" or transaction.status == "RETURNED WITH MISSING" or transaction.status == "RETURNED WITH DAMAGE AND MISSING":
            finished = FinishedTransactions.objects.filter(transaction_id=transaction_id)

            context = {
                "borrower": borrower,
                "transaction": transaction,
                "finished": finished
            }

            return render(request, "tk/transactions/returned.html", context)
            
        elif transaction.status == "VOIDED":
            voided = VoidedTransactions.objects.filter(transaction_id=transaction_id)

            context = {
                "borrower": borrower,
                "transaction": transaction,
                "voided": voided
            }

            return render(request, "tk/transactions/voided.html", context)

    return render(request, 'tk/transaction_details_tk.html', context)

def storages_tk(request):
    try:
        rpi_ip = RpiIP.objects.get(pk=1)
        r = requests.get(f"http://{rpi_ip.ip_address}/checkRPI")
        

    except requests.Timeout:
        return HttpResponseNotFound('<h1>Make Sure that the Raspberry Pi is ON and connected.</h1>')

    s1_count = Tools.objects.filter(storage=1).exclude(is_removed=True).count()
    s2_count = Tools.objects.filter(storage=2).exclude(is_removed=True).count()
    s3_count = Tools.objects.filter(storage=3).exclude(is_removed=True).count()
    s4_count = Tools.objects.filter(storage=4).exclude(is_removed=True).count()
    s5_count = Tools.objects.filter(storage=5).exclude(is_removed=True).count()
    s6_count = Tools.objects.filter(storage=6).exclude(is_removed=True).count()
    s7_count = Tools.objects.filter(storage=7).exclude(is_removed=True).count()
    s8_count = Tools.objects.filter(storage=8).exclude(is_removed=True).count()

    context =  {
        's1_count': s1_count,
        's2_count': s2_count,
        's3_count': s3_count,
        's4_count': s4_count,
        's5_count': s5_count,
        's6_count': s6_count,
        's7_count': s7_count,
        's8_count': s8_count
    }

    return render(request, 'tk/manage_tools/storages_tk.html', context)

def storage_tk(request, storage):
    try:
        rpi_ip = RpiIP.objects.get(pk=1)
        r = requests.get(f"http://{rpi_ip.ip_address}/checkRPI")
        

    except requests.Timeout:
        return HttpResponseNotFound('<h1>Make Sure that the Raspberry Pi is ON and connected.</h1>')

    tools = Tools.objects.filter(storage=storage).exclude(is_removed=True).order_by('layer')
    context =  {
        'tools': tools,
        'storage': storage
    }

    return render(request, 'tk/manage_tools/storage_tk.html', context)


@login_required(login_url='index')
def add_tools_tk(request):
    if request.user.is_authenticated:
        if request.user.role == "STUDENT" or request.user.role == "FACULTY":
                return redirect("home_sf")

    if request.method == "POST":
        try:
            tool_id = request.POST.get('tool_id')
            tool_name = request.POST.get('tool_name')
            tool_image = request.POST.get('tool_img')
            storage = int(request.POST.get('storage'))
            layer = int(request.POST.get('layer'))

            # Modify base 64 image format to save in database
            format, imgstr = tool_image.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr))  
            file_name = tool_id + '.' + ext

            print(Tools.objects.filter(tool_name=tool_name))
            if not Tools.objects.filter(tool_name=tool_name):
                print("!!!!!!!!!")
                ToolQuantity.objects.create(
                    tool_name = tool_name.upper(),
                    quantity=1
                )
            
            if Tools.objects.filter(tool_name=tool_name):    
                tool = ToolQuantity.objects.get(tool_name=tool_name)
                tool.quantity += 1
                tool.save()

            new_tool = Tools.objects.create(
                tool_id = tool_id,
                tool_name = tool_name.upper(),
                storage = storage,
                layer = layer,
            )

            new_tool.tool_image.save(file_name, data, save=True)
            new_tool.save()


            messages.add_message(request, messages.SUCCESS, "TOOL REGISTERED SUCCESSFULLY!")
            context = {"storage": storage}
            return render(request, "tk/manage_tools/add_tools_tk.html", context)
        
        except ValueError:
            messages.add_message(request, messages.ERROR, "NO TOOL IMAGE!", extra_tags="no_image_error")
            return redirect('add_tools_tk')

        except IntegrityError:
            messages.add_message(request, messages.ERROR, "DUPLICATE ENTRY", extra_tags="duplicate_entry_error")
            return redirect('add_tools_tk')

        except requests.Timeout:
            return HttpResponseNotFound('<h1>Make Sure that the Raspberry Pi is ON and connected.</h1>')

    return render(request, 'tk/manage_tools/add_tools_tk.html')


@login_required(login_url='index')
def tools_tk(request):
    if request.user.is_authenticated:
        if request.user.role == "STUDENT" or request.user.role == "FACULTY":
            return redirect("home_sf")
    
    try:
        if request.method == "GET":
            if request.GET.get('tool_id') != None:
                tool_id = int(request.GET.get('tool_id'))
                tool = Tools.objects.get(pk=tool_id)

                if tool.is_removed == False:
                    context =  {
                        'tool': tool
                    }
                    return render(request, 'tk/manage_tools/tools_tk.html', context)
                
                elif tool.is_removed == True:
                    messages.add_message(request, messages.ERROR, "Tool was not registered or has been removed.")
                    return redirect('storages_tk')

            if request.GET.get('rfid') != None:
                tool_id = request.GET.get('rfid')
                tool = Tools.objects.get(pk=tool_id)

                if tool.is_removed == False:
                    context =  {
                        'tool': tool
                    }
                    return render(request, 'tk/manage_tools/tools_tk.html', context)

                elif tool.is_removed == True:
                    messages.add_message(request, messages.ERROR, "Tool was not registered or has been removed.")
                    return redirect('storages_tk')
    
    except Tools.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Tool was not registered or has been removed.")
        return redirect('storages_tk')
    
    if request.method == "POST" and request.POST.get('remove_tool') == "Remove Now":
        try:
            rpi_ip = RpiIP.objects.get(pk=1)
            r = requests.get(f"http://{rpi_ip.ip_address}/checkRPI")
            

        except requests.Timeout:
            return HttpResponseNotFound('<h1>Make Sure that the Raspberry Pi is ON and connected.</h1>')

        tool = Tools.objects.get(pk=int(request.POST.get('remove_tool_id')))
        tool_quantity = ToolQuantity.objects.get(tool_name=tool.tool_name)
        tool_quantity -= 1
        tool.is_removed = True
        tool.status = "REMOVED"
        tool.save()
        tool_quantity.save()

        messages.add_message(request, messages.ERROR, f"Tool with name {tool.tool_name} has been removed!", extra_tags="tool_removed_error")
        return redirect('storage_tk', tool.storage)

    if request.method == "POST" and request.POST.get('maintenance_tool') == "Proceed":
        try:
            rpi_ip = RpiIP.objects.get(pk=1)
            r = requests.get(f"http://{rpi_ip.ip_address}/checkRPI")
            

        except requests.Timeout:
            return HttpResponseNotFound('<h1>Make Sure that the Raspberry Pi is ON and connected.</h1>')
        tool = Tools.objects.get(pk=int(request.POST.get('maintenance_tool_id')))
        tool.is_under_maintenance = True
        tool.status = "UNDER MAINTENANCE/REPAIR"
        tool.save()

        messages.add_message(request, messages.WARNING, "Tool under maintenance or repair!", extra_tags="tool_maintenance_warning")
        return redirect(reverse('tools_tk') + f'?tool_id={tool.pk}')

    if request.method == "POST" and request.POST.get('available_tool') == "Confirm":
        try:
            rpi_ip = RpiIP.objects.get(pk=1)
            r = requests.get(f"http://{rpi_ip.ip_address}/checkRPI")

        except requests.Timeout:
            return HttpResponseNotFound('<h1>Make Sure that the Raspberry Pi is ON and connected.</h1>')

        tool = Tools.objects.get(pk=int(request.POST.get('available_tool_id')))
        tool.is_under_maintenance = False
        tool.status = "AVAILABLE"
        tool.save()

        messages.add_message(request, messages.WARNING, "Tool under maintenance or repair!", extra_tags="tool_maintenance_warning")
        return redirect(reverse('tools_tk') + f'?tool_id={tool.pk}')

    if request.method == "POST" and request.POST.get('remove_missing_tool') == "YES":
        try:
            rpi_ip = RpiIP.objects.get(pk=1)
            r = requests.get(f"http://{rpi_ip.ip_address}/checkRPI")
            

        except requests.Timeout:
            return HttpResponseNotFound('<h1>Make Sure that the Raspberry Pi is ON and connected.</h1>')
        tool = Tools.objects.get(pk=int(request.POST.get('remove_missing_tool_id')))
        tool.is_removed = True
        tool.status = "REMOVED"
        tool.save()

        messages.add_message(request, messages.ERROR, f"Tool with name {tool.tool_name} has been removed!", extra_tags="tool_removed_error")
        return redirect('storage_tk', tool.storage)     
               
    if request.method == "POST" and request.FILES.get('imageUpload'):
        try:
            rpi_ip = RpiIP.objects.get(pk=1)
            r = requests.get(f"http://{rpi_ip.ip_address}/checkRPI")
            

        except requests.Timeout:
            return HttpResponseNotFound('<h1>Make Sure that the Raspberry Pi is ON and connected.</h1>')
        img = request.FILES.get('imageUpload')
        tool = Tools.objects.get(pk=int(request.POST.get('tool_id')))
        tool.tool_image = img
        tool.save()
        messages.add_message(request, messages.SUCCESS, "Tool image updated!", extra_tags="img_change_success")
        return redirect(reverse('tools_tk') + f'?tool_id={tool.pk}')
    
    if request.method == "POST" and request.POST.get('change_tool_name') != None:
        try:
            rpi_ip = RpiIP.objects.get(pk=1)
            r = requests.get(f"http://{rpi_ip.ip_address}/checkRPI")

        except requests.Timeout:
            return HttpResponseNotFound('<h1>Make Sure that the Raspberry Pi is ON and connected.</h1>')
        tool_name = request.POST.get('change_tool_name')
        tool = Tools.objects.get(pk=int(request.POST.get('tool_id_hidden')))
        tool.tool_name = tool_name
        tool.save()

        messages.add_message(request, messages.SUCCESS, "Tool name changed!", extra_tags="name_change_success")
        return redirect(reverse('tools_tk') + f'?tool_id={tool.pk}')
    
    if request.method == "POST" and request.POST.get('select_storage') != "0" and request.POST.get('select_layer') == None:
        try:
            rpi_ip = RpiIP.objects.get(pk=1)
            r = requests.get(f"http://{rpi_ip.ip_address}/checkRPI")
            
            tool_storage = int(request.POST.get('select_storage'))
            tool = Tools.objects.get(pk=int(request.POST.get('location_tool_id')))
            requests.get(f"http://{rpi_ip.ip_address}/S{tool.storage}")
            requests.get(f"http://{rpi_ip.ip_address}/S{tool_storage}")
            tool.storage = tool_storage
            tool.save()

            messages.add_message(request, messages.SUCCESS, "Tool location changed!", extra_tags="location_change_success")
            return redirect(reverse('tools_tk') + f'?tool_id={tool.pk}')

        except requests.Timeout:
            return HttpResponseNotFound('<h1>Make Sure that the Raspberry Pi is ON and connected.</h1>')
    
    if request.method == "POST" and request.POST.get('select_storage') == None and request.POST.get('select_layer') != "0":
        try:
            rpi_ip = RpiIP.objects.get(pk=1)
            r = requests.get(f"http://{rpi_ip.ip_address}/checkRPI")
            
            tool_layer = int(request.POST.get('select_layer'))
            tool = Tools.objects.get(pk=int(request.POST.get('location_tool_id')))
            requests.get(f"http://{rpi_ip.ip_address}/S{tool.storage}")
            tool.layer = tool_layer
            tool.save()

            messages.add_message(request, messages.SUCCESS, "Tool location changed!", extra_tags="location_change_success")
            return redirect(reverse('tools_tk') + f'?tool_id={tool.pk}')

        except requests.Timeout:
            return HttpResponseNotFound('<h1>Make Sure that the Raspberry Pi is ON and connected.</h1>')

    if request.method == "POST" and request.POST.get('select_storage') != "0" and request.POST.get('select_layer') != "0":
        try:
            rpi_ip = RpiIP.objects.get(pk=1)
            r = requests.get(f"http://{rpi_ip.ip_address}/checkRPI")
            
            tool_storage = int(request.POST.get('select_storage'))
            tool_layer = int(request.POST.get('select_layer'))
            tool = Tools.objects.get(pk=int(request.POST.get('location_tool_id')))
            requests.get(f"http://{rpi_ip.ip_address}/S{tool.storage}")
            requests.get(f"http://{rpi_ip.ip_address}/S{tool_storage}")
            tool.storage = tool_storage
            tool.layer = tool_layer
            tool.save()

            messages.add_message(request, messages.SUCCESS, "Tool location changed!", extra_tags="location_change_success")
            return redirect(reverse('tools_tk') + f'?tool_id={tool.pk}')

        except requests.Timeout:
            return HttpResponseNotFound('<h1>Make Sure that the Raspberry Pi is ON and connected.</h1>')

            
    return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required(login_url='index')
def profile_tk(request):
    if request.user.is_authenticated:
        if request.user.role == "STUDENT" or request.user.role == "FACULTY":
            return redirect("home_sf")

    if request.method == 'POST' and request.FILES.get('imageUpload') == None:
        form = EditUserForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Account details has been updated!", extra_tags="details_change_success")
            return redirect('profile_tk')
    
    if request.method == "POST" and request.FILES.get('imageUpload'):
        img = request.FILES.get('imageUpload')
        _user = User.objects.get(pk=request.user.pk)
        _user.user_img = img
        _user.save()
        messages.add_message(request, messages.SUCCESS, "Profile picture updated successfully!", extra_tags="img_change_success")

        return redirect('profile_tk')
    
    form = EditUserForm(instance=request.user)
        
    context = {
        'form': form,
    }

    return render(request, 'tk/profile_tk.html', context)



@login_required(login_url='index')
def change_password_tk(request):
    if request.user.is_authenticated:
        if request.user.role == "STUDENT" or request.user.role == "FACULTY":
            return redirect("home_sf")

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.add_message(request, messages.SUCCESS, "Password changed successfully!", extra_tags="pass_change_success")
            return redirect("profile_tk")
    
    else:
        form = PasswordChangeForm(user=request.user)
    
    context = {
        'form': form
    }
    
    return render(request, 'tk/change_password_tk.html', context)

# Reset Password
def reset_password(request):
    if request.method == 'POST':
        password_form = PasswordResetForm(request.POST)
        
        if password_form.is_valid():
            data = password_form.cleaned_data['email']
            user_email = User.objects.filter(Q(email=data))
            if user_email.exists():
                for user in user_email:
                    subject = 'Password Reset Request'
                    email_temp_name = 'password_reset/email_pass_message.txt'
                    current_site = get_current_site(request)
                    parameters = {
                        'email' : user.email,
                        'first_name' : user.first_name,
                        'username' : user.username,
                        'domain' : current_site.domain,
                        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                        'token' : default_token_generator.make_token(user),
                        'protocol' : 'http', 
                    }

                    message = render_to_string(email_temp_name, parameters)

                    try:
                        send_mail(auth_user=settings.EMAIL_HOST_USER,
                                subject=subject,
                                message=message,
                                from_email='Tool Keeper TUPC',
                                recipient_list=[user.email],
                                fail_silently=False)

                        return redirect('reset_password_sent')
            
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
       
            else:
                messages.add_message(request, messages.ERROR, "Use the registered email of your account.")
                return redirect('reset_password')

    else:
        password_form = PasswordResetForm()
        context = {'pf' : password_form}

    return render(request, 'password_reset/reset_password.html', context)

########## AJAX ##############
def openStorage(request):
    if request.method == "GET":
        # Receive data from ajax and ge the storage value
        storage = request.GET.get('storage')
        rpi_ip = RpiIP.objects.get(pk=1)

        requests.get(f"http://{rpi_ip.ip_address}/S{storage}")
        # Send request to RPI to open specific storage
        return JsonResponse({"message": f"Storage {storage} has opened."}, status=200)

# AJAX request for getting tools to borrow
def scan_tools(request):
    if request.method == "GET" and request.GET.get('rfid') != None:
        rfid = request.GET.get('rfid')
        try:
            get_tool = Tools.objects.get(pk=rfid)
            response = {"message": "Success",
                    "tool_id": get_tool.pk,
                    "tool_name": get_tool.tool_name,
                    "tool_storage": get_tool.storage,
                    "tool_layer": get_tool.layer}
            return JsonResponse(response, status=200)
        
        except Tools.DoesNotExist:
            return JsonResponse({"message": "Not Found"})

    return HttpResponseNotFound("<h1>Page not found</h1>")

    
   