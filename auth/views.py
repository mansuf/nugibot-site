from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponseRedirect
from authlib.integrations.django_client import OAuth
from urllib.parse import urlencode, urlparse

oauth = OAuth()
oauth.register("cognito")

# Create your views here.

# https://auth.capstone-aws.mansuf-cf.my.id/logout?client_id=7pii1hgpfcmlfgvjnvi1srgfdu&response_type=code&scope=email+openid+phone&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fauth%2Flogin_redirect


def login(request: HttpRequest):
    redirect_uri = request.build_absolute_uri("/auth/login_redirect")
    auth_request_uri = oauth.cognito.authorize_redirect(request, redirect_uri)

    parsed = urlparse(auth_request_uri.url)
    if request.get_host() == "capstone-aws.mansuf-cf.my.id":
        print(parsed.params)
        parsed.params = parsed.params["redirect_uri"].replace("http", "https")

    print(parsed)

    return HttpResponseRedirect(parsed.geturl())


def login_redirect(request: HttpRequest):
    token = oauth.cognito.authorize_access_token(request)
    request.session["user"] = token["userinfo"]
    return redirect("/")


def logout(request: HttpRequest):
    if request.get_host() == "capstone-aws.mansuf-cf.my.id":
        scheme = "https"
    else:
        scheme = "http"

    base_url = "https://auth.capstone-aws.mansuf-cf.my.id/logout?"
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
