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


def diet(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "diet.html", context)


def history(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "history.html", context)


def calculator(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "kalku.html", context)


def track(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "track.html", context)


def vegan(request: HttpRequest):
    context = get_userinfo_context(request)

    return render(request, "vegan.html", context)
