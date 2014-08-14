from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Post(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    user = models.ForeignKey(User)
    is_visible = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.name

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True, null=True)

    post = models.ForeignKey(Post)
    
    activation_code = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=False)


    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    
    def __unicode__(self):
        try:
            return_val = "%s:%s"%(self.user.username, self.comment[:10])
        except AttributeError:
            return_val = "Anon: %s" %self.comment[:10]
        return return_val
