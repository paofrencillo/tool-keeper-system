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
    
class UserRegistrationForm(UserCreationForm):
    COURSES = [('BSCE', 'BS - Civil Engineering'),
                ('BSEE', 'BS - Electrical Engineering'),
                ('BSME', 'BS - Mechanical Engineering'),
                ('BET-ET', 'BET - Electrical Technology'),
                ('BET-ESET', 'BET - Electronics Technology Track: Industrial Automation Technology'),
                ('BET-COET', 'BET - Computer Engineering Technology'),
                ('BET-CT', 'BET - Civil Technology'),
                ('BET-MT', 'BET - Mechanical Technology'),
                ('BET-AT', 'BET - Mechanical Engineering Technology Track: Automative Technology'),
                ('BET-PPT', 'BET - Mechanical Engineering Technology Track: Power Plant Technology'),
                ('BSIE-ICT', 'BSIE - Information and Communication Technology'),
                ('BTTE-AU', 'BTTE - Automative'),
                ('BTTE-EL', 'BTTE - Electrical'),
                ('BTTE-E', 'BTTE - Electronics'),
                ('BTTE-HVACT', 'BTTE - Heating, Ventilation, and Air Conditioning'),
                ('BTTE-CP', 'BTTE - Computer Programming')]

    first_name = forms.CharField(widget=forms.TextInput(
                                attrs={"placeholder": "First Name"}),
                                required=True)
    last_name = forms.CharField(widget=forms.TextInput(
                                attrs={"placeholder": "First Name"}),
                                required=True)
    year_course = forms.CharField(widget=forms.Select(choices=COURSES),
                                    empty_value="Year and Course")
    role = forms.CharField()
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