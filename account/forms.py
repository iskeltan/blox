from django import forms 
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from account.models import UserProfile
from blox.tasks import send_user_activation_mail
import hashlib
import ipdb
import re


class LoginForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['email','password']
        widgets = {
           'password': forms.PasswordInput(),
       }

class RegisterForm(forms.ModelForm):
    password_c = forms.CharField(label=_("confrim password"), widget=forms.PasswordInput())
    bio = forms.CharField(widget=forms.Textarea)


    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
    def clean_password_c(self):
        password = self.cleaned_data["password"]
        password_c = self.cleaned_data["password_c"]

        if password != password_c:
            raise forms.ValidationError(_("These passwords don't match."))

        return password_c

    def clean_email(self):
        email = self.cleaned_data["email"]
        rule = "[^@]+@[^@]+\.[^@]+"
        if not re.match(rule, email):
            raise forms.ValidationError(_("this email is not valid"))
        user = User.objects.filter(email=email)
        if user:
            raise forms.ValidationError(_("this email already used"))

        return email

    def save(self):
        email = self.cleaned_data["email"]
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        password = self.cleaned_data["password"]
        password_c = self.cleaned_data["password_c"]
        bio = self.cleaned_data["bio"]
        random_username = hashlib.sha224(email).hexdigest()[:30]
        activation_code = hashlib.sha224(email).hexdigest()[:50]
        
        user = User()
        user.username = random_username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = False
        user.set_password(password)
        user.save()

        user_profile = UserProfile()
        user_profile.bio = bio
        user_profile.user = user
        user_profile.activation_code = activation_code
        user_profile.save()
        send_user_activation_mail.delay(activation_code, email)


class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ["bio", "avatar" ]


class UserPasswordChangeForm(forms.Form):
    password = forms.CharField(label=_("old password"), widget=forms.PasswordInput())
    new_password = forms.CharField(label=_("new password"), widget=forms.PasswordInput())
    new_password_c = forms.CharField(label=_("new password (confrim)"), widget=forms.PasswordInput())

