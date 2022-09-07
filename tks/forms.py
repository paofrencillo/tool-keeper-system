from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


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
                                    empty_value="Year and Course",
                                    default=None)
    role = forms.CharField()
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}),
                            required=True)

    username = forms.CharField(required=True)
                                
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput,
                                required=True)

    password2 = forms.CharField(label="Confirm Password",
                                widget=forms.PasswordInput,
                                required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "year_course", "role", "email", "username",
                "password1", "password2",]


class ToolRegistrationForm(forms.ModelForm):
    pass
    class Meta:
        pass


class BorrowingForm:
    pass

    class Meta:
        pass

    
