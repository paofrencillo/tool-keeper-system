import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(label='',
                                widget=forms.TextInput(attrs={"placeholder": "Username"}),
                                required=True)
    password = forms.CharField(label='',
                                widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
                                required=True)
    
class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='',
                                widget=forms.TextInput(
                                attrs={"placeholder": "First Name"}),
                                required=True)
    last_name = forms.CharField(label='',
                                widget=forms.TextInput(
                                attrs={"placeholder": "Last Name"}),
                                required=True)
    role = forms.CharField(label='',widget=forms.TextInput(attrs=
                            {'value': 'STUDENT', 'type': 'hidden'}),
                            required=True)
    year_course = forms.CharField(label='',
                                widget=forms.TextInput(attrs={"placeholder": "Year and Course (e.g. BET-COET-NS-1B)"} ),
                                required=True)
    tupc_id = forms.IntegerField(label='',
                                widget=forms.NumberInput(attrs=
                                {'placeholder': 'TUP-C ID (e.g. 190000)'}),
                                required=True)
    email = forms.EmailField(label='',
                            widget=forms.EmailInput(attrs=
                            {"placeholder": "Email"}),
                            required=True)
    username = forms.CharField(label='',
                            widget=forms.TextInput(attrs={"placeholder": "Username"}),
                            required=True)                           
    password1 = forms.CharField(label='',
                            widget=forms.PasswordInput(attrs=
                            {"placeholder": "Password"}),
                            required=True)
    password2 = forms.CharField(label='',
                                widget=forms.PasswordInput(attrs=
                                {"placeholder": "Confirm Password"}),
                                required=True)
    class Meta:
        model = User
        fields = ["first_name", "last_name", "year_course", "tupc_id", "role", "email", "username",
                "password1", "password2",]


class FacultyRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(
                                attrs={"placeholder": "First Name"}),
                                required=True)
    last_name = forms.CharField(widget=forms.TextInput(
                                attrs={"placeholder": "Last Name"}),
                                required=True)
    year_course = forms.CharField(widget=forms.TextInput(attrs={'value': '', 'type': 'hidden'}),
                                    required=True)
    role = forms.CharField(widget=forms.TextInput(attrs={'value': 'FACULTY', 'readonly': True}),
                            required=True)
    tupc_id = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': '000000'}),
                                required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}),
                            required=True)
    username = forms.CharField(required=True)                           
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
                                required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
                                required=True)
    class Meta:
        model = User
        fields = ["first_name", "last_name", "year_course", "role", "email", "username",
                "password1", "password2",]

class ToolKeeperRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(
                                attrs={"placeholder": "First Name"}),
                                required=True)
    last_name = forms.CharField(widget=forms.TextInput(
                                attrs={"placeholder": "Last Name"}),
                                required=True)
    year_course = forms.CharField(widget=forms.TextInput(attrs={'value': '', 'type': 'hidden'}),
                                    required=True)
    role = forms.CharField(widget=forms.TextInput(attrs={'value': 'TOOL KEEPER', 'readonly': True}),
                            required=True)
    tupc_id = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': '000000'}),
                                required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}),
                            required=True)
    username = forms.CharField(required=True)                           
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
                                required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
                                required=True)
    class Meta:
        model = User
        fields = ["first_name", "last_name", "year_course", "role", "email", "username",
                "password1", "password2",]
class ToolRegistrationForm(forms.ModelForm):
    tool_id = forms.IntegerField(required=True)
    tool_name = forms.CharField(required=True)
    tool_image = forms.ImageField(required=True)
    storage = forms.CharField(required=True)
    layer = forms.CharField(required=True)
    class Meta:
        model = Tools
        fields = ["tool_id", "tool_name", "tool_image", "storage", "layer"]

class ToolReservationForm:
    class Meta:
        model = Transactions
        fields = ["borrower_id", "fullname", "year_course", "borrow_datetime", "return_datetime"]