#-*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.core.cache import cache
from django.contrib import messages
from post.models import Post, Comment
from post.forms import CommentForm, CommentForm_no_auth, \
        PostAddForm
from blox.tasks import send_comment_activation_mail
import ipdb
import copy


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

    ctx = { "post": post, "comment_form": comment_form, "all_comments": all_comments }
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
            messages.info(request, _("your comment has been added"))
        else:
            comment_form = CommentForm_no_auth(request.POST, initial=initial_data)
            messages.info(request, _("your comment has been added but must confirm with email required "))

        if comment_form.is_valid():
            comment_form.save()
            return HttpResponseRedirect(reverse("detail", args=[post_id]))
        else:
            messages.warning(request, _("this comment is not valid "))
            return HttpResponseRedirect(reverse("detail", args=[post_id]))
    else:
        return HttpResponseRedirect("/")



def activate_comment(request, activation_code):
    comment = Comment.objects.filter(activation_code=activation_code)
    if comment:
        comment = comment[0]
        comment.is_active = True
        comment.save()
        messages.info(request, _("your comment has been activated"))
    else:
        messages.error(request, _("invalid activation key"))

    return HttpResponseRedirect(reverse('detail', args=[comment.post.id]))


@login_required(login_url='/account/profile/')
def add_post(request):
    if request.method == "POST":
        form = PostAddForm(request.POST)
        if form.is_valid():
            post_name = form.cleaned_data["name"]
            post_content = form.cleaned_data["content"]
            post = Post()
            post.name = post_name
            post.content = post_content
            post.user = request.user
            post.is_visible = True
            post.save()
            return HttpResponseRedirect(reverse('detail', args=[post.pk]))
        else:
            messages.error(request, _("form is not valid"))

        ctx = {"form": form }
    else:
        form = PostAddForm()
        ctx = {"form": form} 
    return render(request, "add_post.html", ctx)


@login_required(login_url='/account/profile/')
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = PostAddForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.info(request, _("post update is successful"))
            return HttpResponseRedirect(reverse("edit_post", args=[post.id]))
        else:
            messages.warning(request, _("post update is unsuccessful"))
            return HttpResponseRedirect(reverse("edit_post", args=[post.id]))
    else:
        if not post.user == request.user:
            messages.warning(request, _("this post not yours"))
            return HttpResponseRedirect(reverse("user_profile"))

    form = PostAddForm(instance=post)

    ctx = {"form": form, "post_id": post_id}
    return render(request, "edit_post.html", ctx)
