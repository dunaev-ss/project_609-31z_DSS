from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.contrib.auth import password_validation


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control mb-3"}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "class": "form-control mb-3"}),
    )


class SignupForm(UserCreationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control mb-3"}))
    password1 = forms.CharField(
        label="Password",
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control mb-3"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control mb-3"}),
        help_text="Enter the same password as before, for verification.",
    )
