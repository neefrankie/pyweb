from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import SignUpForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from .models import User, PasswordResetter


# Create your views here.


def signup(request: HttpRequest):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = User.from_email(email=email, pw=password)

            user.save()
            return HttpResponseRedirect(reverse("main:home"))
    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


def login(request: HttpRequest):
    error_message = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            print(email, password)
            user = User.objects.get(email=email)
            if user:
                if user.is_password_matched(password):
                    return HttpResponseRedirect(reverse("main:home"))
                else:
                    error_message = "Incorrect password"
            else:
                error_message = "User not found"

    else:
        form = LoginForm()

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
            "error_message": error_message,
        },
    )


# Form to send password reset letter
# /password-reset
def password_reset_email(request: HttpRequest):
    error_message = None
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        # If not true, will go back to the template with the form.
        # This time the form is no longer empty so the HTML form
        # will be populated with the data previously submitted.
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.get(email=email)
            if user:
                resetter = PasswordResetter()
                resetter.user = user
                resetter.save()
                return HttpResponseRedirect(reverse("accounts:password_reset_done"))
            else:
                error_message = "Email does not exist"
    else:
        form = ForgotPasswordForm()

    return render(
        request,
        "accounts/password_reset_email.html",
        {
            "error_message": error_message,
            "form": form
        },
    )


# Message shown after email is sent to user.
# /password-reset/done
def password_reset_done(request: HttpRequest):
    return render(
        request,
        "accounts/password_reset_done.html",
    )


# Verify password reset token and show reset form if token valid.
# /reset/<token>
def password_reset_confirm(request: HttpRequest, token: str):
    if request.method == "POST":
        form = ResetPasswordForm()
        if form.is_valid():
            print(form.cleaned_data)

        return HttpResponseRedirect(reverse("account:password_reset_complete"))
    else:
        form = ResetPasswordForm()
        resetter = PasswordResetter.objects.get(token=token)
        if not resetter:
            return render(
                request,
                "accounts/password_reset_invalid_token.html"
            )
        elif resetter.is_expired():
            print('resetter expired')
            return render(
                request,
                "accounts/password_reset_invalid_token.html"
            )

    return render(
        request,
        "accounts/password_reset_confirm.html",
        {
            "form": form,
            "token": token,
            "email": resetter.user.email
        }
    )


# /reset/done
def password_reset_complete(request: HttpRequest):
    return render(
        request,
        "accounts/password_reset_complete.html",
    )
