from django.http import HttpRequest
from django.shortcuts import render
from utils.userinfo import get_userinfo_context

from .models import CommunityPost, CommunityPostComment

# Create your views here.


def vegan(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "vegan.html", context)


def diet(request: HttpRequest):
    context = get_userinfo_context(request)

    posts = []

    for post in CommunityPost.objects.all():
        post.comments = CommunityPostComment.objects.filter(post=post)
        post.total_comments = len(post.comments) | 0

        posts.append(post)

    context["posts"] = posts
    context["comments"] = CommunityPost

    return render(request, "diet.html", context)
