from django.shortcuts import render
from django.http import HttpRequest

# Create your views here.


def get_userinfo_context(request: HttpRequest):
    userinfo = request.session.get("user", None)
    context = {"user": userinfo}

    if userinfo:
        context["username"] = userinfo["cognito:username"]
        context["email"] = userinfo["email"]

    return context


def home(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "index.html", context)


def about(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "about.html", context)


def community(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "community.html", context)


def contact(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "contact.html", context)


def team(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "team.html", context)


def testimonial(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "testimonial.html", context)
