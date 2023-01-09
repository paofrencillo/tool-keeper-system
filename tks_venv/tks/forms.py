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
                                attrs={"placeholder": "First Name", "autofocus": True}),
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
                            widget=forms.TextInput(attrs={"placeholder": "Username", "autofocus": False}),
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
    first_name = forms.CharField(label='', widget=forms.TextInput(
                                attrs={"placeholder": "First Name", "autofocus": True}),
                                required=True)
    last_name = forms.CharField(label='', widget=forms.TextInput(
                                attrs={"placeholder": "Last Name"}),
                                required=True)
    role = forms.CharField(label='', widget=forms.TextInput(attrs={'value': 'FACULTY', 'readonly': True}),
                            required=True)
    tupc_id = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'placeholder': 'TUP-C ID (e.g. 000000)'}),
                                required=True)
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={"placeholder": "Email"}),
                            required=True)
    username = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "Username"}), required=True)                           
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
                                required=True)
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
                                required=True)
    class Meta:
        model = User
        fields = ["first_name", "last_name", "tupc_id", "role", "email", "username",
                "password1", "password2",]

class ToolKeeperRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(
                                attrs={"placeholder": "First Name", "autofocus": True}),
                                required=True)
    last_name = forms.CharField(label='', widget=forms.TextInput(
                                attrs={"placeholder": "Last Name"}),
                                required=True)
    role = forms.CharField(label='', widget=forms.TextInput(attrs={'value': 'TOOL KEEPER', 'readonly': True}),
                            required=True)
    tupc_id = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'placeholder': 'TUP-C ID (e.g. 000000)'}),
                                required=True)
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={"placeholder": "Email"}),
                            required=True)
    username = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "Username",
                                "autofocus": False}), required=True)                           
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
                                required=True)
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
                                required=True)
    class Meta:
        model = User
        fields = ["first_name", "last_name", "tupc_id", "role", "email", "username",
                "password1", "password2",]

class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(label="Firstname",
                                max_length=255,
                                required=False)
    last_name = forms.CharField(label="Lastname",
                                max_length=255,
                                required=False)
    role = forms.CharField(label='Registered as',
                            widget=forms.TextInput(attrs={'readonly': ''}),
                            required=False)
    tupc_id = forms.IntegerField(label='TUPC ID',
                                widget=forms.NumberInput(attrs={'readonly': ''}),
                                required=False)
    email = forms.EmailField(label="Email Address",
                            max_length=255,
                            required=False)

    username = forms.CharField(label="Username",
                                max_length=255,
                                required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'role', 'tupc_id','email', 'username']


class ChangePasswordForm(forms.Form):
    password = forms.CharField(label="New Password",
                                widget=forms.PasswordInput(attrs={'readonly': ''}),
                                max_length=255,
                                required=True)
    cpassword = forms.CharField(label="Confirm New Password",
                                widget=forms.PasswordInput(attrs={'readonly': ''}),
                                max_length=255,
                                required=True)

    def clean_cpassword(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("cpassword")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )