import hashlib
from django import forms 
from django.contrib.contenttypes.models import ContentType
from post.models import Post, Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment', 'email']
        widgets = {
            "comment" : forms.Textarea(attrs={"placeHolder":"Yorumunuz"}),
            "email" : forms.TextInput(attrs={"placeHolder":"Email Adresiniz",}),
        }


#    def __init__(self, *args, **kwargs):
#        my_user = kwargs.pop('my_user', None)
#        if my_user:
#            super(CommentForm, self).__init__(*args, **kwargs)
#            if my_user.is_authenticated():
#                del self.fields['email']
#
#
#    def save(self, user, post, parent_object):
#        form_comment = self.cleaned_data["comment"]
#        if user.is_authenticated():
#            new_comment = Comment()
#            new_comment.user = user
#            new_comment.comment = form_comment
#            new_comment.post = post
#            new_comment.email = user.email
#            new_comment.object_id = parent_object.id
#            new_comment.content_type = ContentType.objects.get_for_model(parent_object)
#            new_comment.is_active = True
#            new_comment.activation_code = 0
#            new_comment.save()
#        else:
#            form_email = self.cleaned_data["email"]
#            activation_code = hashlib.sha224(form_email).hexdigest()[:50]
#
#            new_comment = Comment()
#            new_comment.comment = form_comment
#            new_comment.post = post
#            new_comment.email = form_email
#            new_comment.object_id = parent_object.id
#            new_comment.content_type = ContentType.objects.get_for_model(parent_object)
#            new_comment.activation_code = activation_code
#            new_comment.is_active = False
#            new_comment.save()
#
#			    #TODO: send_activate_comment_mail.delay(activation_code, form_email)
#
