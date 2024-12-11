from django.http import HttpRequest
from django.shortcuts import render
from utils.userinfo import get_userinfo_context

from .models import CommunityPost, CommunityPostComment

# Create your views here.


def vegan(request: HttpRequest):
    context = get_userinfo_context(request)

    posts = []

    for post in CommunityPost.objects.filter(parent="vegan"):
        post.comments = CommunityPostComment.objects.filter(post=post)
        post.total_comments = len(post.comments) | 0

        posts.append(post)

    context["parent"] = "Vegan"
    context["posts"] = posts
    context["comments"] = CommunityPost

    return render(request, "community_posts.html", context)


def diet(request: HttpRequest):
    context = get_userinfo_context(request)

    posts = []

    for post in CommunityPost.objects.filter(parent="diet"):
        post.comments = CommunityPostComment.objects.filter(post=post)
        post.total_comments = len(post.comments) | 0

        posts.append(post)

    context["parent"] = "Diet"
    context["posts"] = posts
    context["comments"] = CommunityPost

    return render(request, "community_posts.html", context)
