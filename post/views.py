#-*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.cache import cache
from post.models import Post, Comment
from post.forms import CommentForm, CommentForm_no_auth
from blox.tasks import send_comment_activation_mail

def home(request):
    posts = cache.get("all_post")
    if not posts:
        posts = Post.objects.filter(is_visible=True).order_by("-updated_at")[:15]
        cache.set("all_post", posts)
    ctx = { "posts": posts }
#    send_comment_activation_mail.delay("1324","iskeltan8@gmail.com")
    return render(request, "index.html", ctx)
    #return HttpResponse("Jello World!")


def detail(request, post_id):
    post = cache.get("post-%s" %post_id)
    if not post:
        post = get_object_or_404(Post, pk=post_id)
        cache.set("post-%s"%post_id, post)

    if request.user.is_authenticated():
        comment_form = CommentForm()
    else:
        comment_form = CommentForm_no_auth()

    all_comments = cache.get("post_comment-%s"%post_id)
    if not all_comments:
        all_comments = Comment.objects.filter(is_active=True, post=post)
        cache.set("post_comment-%s"%post_id, all_comments)
    ctx = { "post": post, "comment_form": comment_form, "all_comments": all_comments  }
    return render(request, "detail.html", ctx)


def add_comment(request, post_id, obj_name, obj_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        if obj_name == "post":
            parent_object = post
        elif obj_name == "comment":
            parent_object = get_object_or_404(Comment, pk=obj_id)
        else:
            return HttpResponseRedirect("/?err=postmucommentmiparentin")
        
        initial_data = {"post": post, "parent_object": parent_object, "user": request.user }

        if request.user.is_authenticated():
            comment_form = CommentForm(request.POST, initial=initial_data)
            print "auth"
        else:
            comment_form = CommentForm_no_auth(request.POST, initial=initial_data)
            print "not auth"

        if comment_form.is_valid():
            comment_form.save()
            return HttpResponseRedirect(reverse("detail", args=[post_id]))
        else:
            return HttpResponseRedirect(reverse("detail", args=[post_id]))

        return HttpResponse("postla geldi")
    else:
        return HttpResponseRedirect("/")
