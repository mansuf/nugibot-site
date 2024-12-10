from django.shortcuts import redirect
from django.http import HttpRequest
from authlib.integrations.django_client import OAuth
from urllib.parse import urlencode

oauth = OAuth()
oauth.register("cognito")

# Create your views here.


def login(request: HttpRequest):
    redirect_uri = request.build_absolute_uri("/auth/login_redirect")

    if request.get_host() == "www.nugibot.my.id":
        redirect_uri = redirect_uri.replace("http", "https")

    auth_request_uri = oauth.cognito.authorize_redirect(request, redirect_uri)
    return auth_request_uri


def login_redirect(request: HttpRequest):
    token = oauth.cognito.authorize_access_token(request)
    request.session["user"] = token["userinfo"]
    return redirect("/")


def logout(request: HttpRequest):
    if request.get_host() == "www.nugibot.my.id":
        scheme = "https"
    else:
        scheme = "http"

    base_url = "https://auth.nugibot.my.id/logout?"
    query_params = urlencode(
        {
            "client_id": oauth.cognito.client_id,
            "logout_uri": f"{scheme}://{request.get_host()}/auth/logout_redirect",
        }
    )

    request.session.pop("user", None)
    return redirect(base_url + query_params)


def logout_redirect(request: HttpRequest):
    request.session.pop("user", None)
    return redirect("/")
