from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    bio = models.TextField()
    avatar = models.ImageField(upload_to='static/avatar/')
    activation_code = models.CharField(max_length=50)


    def create_user_profile(instance, **kwargs):
        pass
