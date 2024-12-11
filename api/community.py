from django.http import JsonResponse, HttpRequest
from community.models import CommunityPost
from utils.userinfo import get_userinfo_context


def create_community_post(request: HttpRequest):
    userinfo = get_userinfo_context(request)

    if not userinfo["user"]:
        return JsonResponse({"error": "User not logged in"}, status=403)

    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = request.POST
    files = request.FILES

    try:
        post = CommunityPost(
            parent=data["parent"],
            author=userinfo["username"],
            content_text=data["text"],
            likes=0,
        )

        if files.get("image"):
            post.content_image = files["image"]

        post.save()
    except KeyError as e:
        return JsonResponse({"error": f"Missing key = {e}"}, status=400)

    return JsonResponse({"success": "ok"})
