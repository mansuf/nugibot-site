from django.shortcuts import render, redirect
from django.http import HttpRequest
from utils.userinfo import get_userinfo_context

# Create your views here.


def home(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "index.html", context)


def about(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "about.html", context)


def community(request: HttpRequest):
    return redirect("/community/vegan")


def contact(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "contact.html", context)


def team(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "team.html", context)


def testimonial(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "testimonial.html", context)


def article(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "article.html", context)


def article2(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "article2.html", context)


def article3(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "article3.html", context)


def chart(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "chart.html", context)


def chatbot(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "chatbot.html", context)


def history(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "history.html", context)


def calculator(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "kalku.html", context)


def track(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "track.html", context)
