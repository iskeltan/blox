from django import forms 
from django.contrib.contenttypes.models import ContentType
from post.models import Post, Comment
from blox.tasks import send_comment_activation_mail
import hashlib
import random
import re


class CommentForm_no_auth(forms.ModelForm):


    class Meta:
        model = Comment
        fields = ['comment', 'email']
        widgets = {
            "comment" : forms.Textarea(attrs={"placeHolder":"write a comment"}),
            "email" : forms.TextInput(attrs={"placeHolder":"E-Mail Address"}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        rule = "[^@]+@[^@]+\.[^@]+"
        if not re.match(rule, email):
            raise forms.ValidationError(_("this email is not valid"))

        return email


    def save(self):
        post = self.initial["post"]
        parent_object = self.initial["parent_object"]
        email = self.cleaned_data["email"]
        random_int = random.random()*9999
        activation_code = hashlib.sha224("%s:%s"%(email,random_int)).hexdigest()[:50]
        print activation_code
        new_comment = Comment()
        new_comment.comment = self.cleaned_data["comment"]
        new_comment.email = email 
        new_comment.post = post
        new_comment.activation_code = activation_code
        new_comment.object_id = parent_object.id
        new_comment.content_type = ContentType.objects.get_for_model(parent_object)
        new_comment.is_active = False
        new_comment.save()
        send_comment_activation_mail.delay(activation_code, email)

class CommentForm(forms.ModelForm):
    
    
    class Meta:
        model = Comment

        fields = ['comment']
        widgets = {
            "comment": forms.Textarea(attrs={"placeHolder":"write a comment"})
        }
    
    def save(self):
        post = self.initial["post"]
        user = self.initial["user"]
        parent_object = self.initial["parent_object"]


        new_comment = Comment()
        new_comment.comment = self.cleaned_data["comment"]
        new_comment.post = post
        new_comment.user = user
        new_comment.object_id = parent_object.id
        new_comment.content_type = ContentType.objects.get_for_model(parent_object)
        new_comment.is_active = True
        new_comment.activation_code = 0
        new_comment.save()



#    def __init__(self,my_user=False, *args, **kwargs):
##        my_user = kwargs.get("my_user", None)
#        if my_user:
#            super(CommentForm, self).__init__(*args, **kwargs)
#            if my_user.is_authenticated():
#                del self.fields["email"]
#        else:
#            super(CommentForm, self).__init__(*args, **kwargs)
#
#    def save(self, user, post, parent_object):
#        form_comment = self.cleaned_data["comment"]
#        new_comment = Comment()
#        new_comment.comment = form_comment
#        new_comment.post = post
#        new_comment.object_id = parent_object.id
#        new_comment.content_type = ContentType.objects.get_for_model(parent_object)
#        
#        if user.is_authenticated():
#            new_comment.user = user
#            new_comment.email = user.email
#            new_comment.is_active = True
#            new_comment.activation_code = 0
#        else:
#            form_email = self.cleaned_data["email"]
#            activation_code = hashlib.sha224(form_email).hexdigest()[:50]
#
#            new_comment.email = form_email
#            new_comment.is_active = False
#            new_comment.activation_code = activation_code
#
#        new_comment.save()
