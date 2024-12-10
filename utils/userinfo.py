from django.http import HttpRequest


def get_userinfo_context(request: HttpRequest):
    userinfo = request.session.get("user", None)
    context = {"user": userinfo}

    if userinfo:
        context["username"] = userinfo["cognito:username"]
        context["email"] = userinfo["email"]

    return context
