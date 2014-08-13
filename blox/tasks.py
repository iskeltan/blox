from celery import task
from django.core.mail import EmailMessage
from post.models import Post

@task
def send_comment_activation_mail(activation_key, email_address):
    subject = "Comment Activation"
    body = "click <a href='/'>here</a> for activate your comment"
    from_email = "bloxmarkafoni@gmail.com"
    
    email = EmailMessage(subject, body, to=[email_address], headers={"content_type":"text/html"})
    email.send()


@task
def send_user_activation_mail(activation_key, email_address):
    subject = "About your user activation"
    body = "go to this link for user activation: http://localhost/activate/account/%s/" %activation_key
    email = EmailMessage(subject, body, to=[email_address], headers={"content_type":"text/html"})
    email.send()
