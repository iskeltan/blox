#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from account.forms import LoginForm, RegisterForm, UserProfileForm
from account.models import UserProfile
import ipdb

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                    form = LoginForm(request.POST)
                    messages.warning(request, "this user is not active")
                    ctx = { "login_form": form}
                    return render(request, "login.html", ctx)
            else:
                form = LoginForm(request.POST)
                form.errors["email"] = _("boyle bir kullanici yok")
                messages.error(request, "no such user")
                ctx = { "login_form": form}
                return render(request, "login.html", ctx)
        else:
            form = LoginForm(request.POST)
            ctx = {"login_form": form }
            return render(request, "login.html", ctx)
    else:
        form = LoginForm()
        ctx = { "login_form": form}
        return render(request, "login.html", ctx)


def logout_view(request):
    if request.GET.get('im') == 'sure':
        logout(request)
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponse("are you seriously :( ? \
        <br> <a href='?im=sure'>yes</a> <a href='/'>no</a>")


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, _("your user has been created but need confirm email"))
            return HttpResponseRedirect(reverse('home'))
        else:
            form = RegisterForm(request.POST)
            ctx = {"register_form": form }
            return render(request, "register.html", ctx)
    else:
        form = RegisterForm()
        ctx = {"register_form" : form }
        return render(request, "register.html", ctx)


def activate_user(request, activation_code):
    activation_code = ''.join(activation_code)
    if not activation_code:
        return HttpResponse('invalid code')
    print activation_code

    user_profile = UserProfile.objects.filter(activation_code=activation_code)
    if user_profile:
        user_profile = user_profile[0]
    else:
        messages.error(request, _("this code does not belong to a user"))
        return HttpResponseRedirect(reverse('home'))
    if user_profile.user.is_active:
        messages.info(request, _("this user is already activated"))
        return HttpResponseRedirect(reverse('home'))
    user_profile.user.is_active = True
    user_profile.user.save()
    messages.info(request, "activate your account")
    return HttpResponseRedirect(reverse('home'))



@login_required(login_url='/account/login/')
def user_profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user_profile'))
        else:
            ctx = {"form": form}
            return render(request, "user_profile.html", ctx )
    else:
        form = UserProfileForm()
        ctx = {"form": form}
        return render(request, "user_profile.html", ctx)
