import PIL
from celery import task
from django.core.mail import EmailMessage
from post.models import Post
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
from PIL import Image


@task
def send_comment_activation_mail(activation_key, email_address):
    site = Site.objects.get_current().domain
    subject = _("Comment Activation")
    body = "%s:  http://%s/comment/activate/%s "%(_("go to this link for activate your comment"), site, \
            activation_key)
    email = EmailMessage(subject, body, to=[email_address], headers={"content_type":"text/html"})
    email.send()


@task
def send_user_activation_mail(activation_key, email_address):
    site = Site.objects.get_current().domain
    subject = _("About your user activation")
    body = "%s: http://%s/account/activate/%s/" %(_("go to this link for user activation"),site, \
            activation_key)
    email = EmailMessage(subject, body, to=[email_address], headers={"content_type":"text/html"})
    email.send()


@task
def crop_image(image_path):
    basewidth = 300

    img = Image.open(image_path)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
    img.save(image_path)
