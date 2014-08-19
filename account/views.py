#-*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User, check_password
from django.contrib.auth.decorators import login_required
from account.forms import LoginForm, RegisterForm, UserProfileForm, \
         UserPasswordChangeForm
from account.models import UserProfile
from post.models import Post
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
                    messages.warning(request, _("this user is not active"))
                    ctx = { "login_form": form}
                    return render(request, "login.html", ctx)
            else:
                form = LoginForm(request.POST)
                form.errors["email"] = _("no such user")
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


@login_required        
def logout_view(request):
    if request.GET.get('im') == 'sure':
        logout(request)
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponse("are you serious :( ? \
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
        return HttpResponse(_('invalid code'))
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
    messages.info(request, _("activate your account"))
    return HttpResponseRedirect(reverse('home'))



@login_required
def user_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect(reverse('user_profile'))
        else:
            ctx = {"profile_form": profile_form}
            return render(request, "user_profile.html", ctx )
    else:
        user_post = Post.objects.filter(user=request.user)
        profile_form = UserProfileForm(instance=user_profile)
        password_change_form = UserPasswordChangeForm()
        ctx = {"profile_form": profile_form, "posts": user_post,
            "password_change_form": password_change_form }
        return render(request, "user_profile.html", ctx)


@login_required        
def password_change(request):
    if request.method == "POST":
        form = UserPasswordChangeForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data["password"]
            new_password = form.cleaned_data["new_password"]
            new_password_c = form.cleaned_data["new_password_c"]
            if not request.user.check_password(old_password): 
                messages.warning(request, _("old password not matching"))
                return HttpResponseRedirect(reverse('user_profile'))
            if not new_password == new_password_c:
                messages.warning(request, _("passwords not matching"))
                return HttpResponseRedirect(reverse('user_profile'))
            user = User.objects.get(id=request.user.id)
            user.set_password(new_password)
            user.save()
            messages.info(request, _("password change successful"))
            return HttpResponseRedirect(reverse("user_profile"))
        else:
            messages.warning(request, _("form is not valid"))
            return HttpResponseRedirect(reverse("user_profile"))
    else:
        return HttpResponseRedirect(reverse("user_profile"))
