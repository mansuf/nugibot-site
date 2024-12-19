from django.http import HttpRequest, HttpResponse, StreamingHttpResponse, JsonResponse
from .bedrock import iter_response_chatbot
from .dynamodb import query_chat_history
from .utils import generate_presigned_url

from utils.userinfo import get_userinfo_context


def get_chatbot_response(request: HttpRequest):
    userinfo = get_userinfo_context(request)

    if not userinfo["user"]:
        return HttpResponse("Error: User not logged in", status=403)

    if request.method != "POST":
        return HttpResponse("Error: Method not allowed", status=405)

    try:
        # Get form data
        prompt = request.POST.get("prompt")
        session_id = request.POST.get("session_id")

        if not prompt:
            return HttpResponse("Error: Missing prompt", status=400)
        if not session_id:
            return HttpResponse("Error: Missing session_id", status=400)

        # Handle image if present
        image_file = None
        image_format = None
        if "image" in request.FILES:
            image_file = request.FILES["image"]

            # Validate file type
            allowed_types = [
                "image/jpeg",
                "image/jpg",
                "image/png",
                "image/gif",
                "image/webp",
            ]

            if image_file.content_type not in allowed_types:
                return HttpResponse(
                    "Error: Invalid file type. Allowed types: JPEG, PNG, GIF, WebP",
                    status=400,
                )

            # Validate file size (5MB limit)
            if image_file.size > 5 * 1024 * 1024:
                return HttpResponse("Error: File too large. Maximum size: 5MB", status=400)

            image_format = image_file.content_type.replace("image/", "")

        # Return streaming response with image URL if available
        return StreamingHttpResponse(
            iter_response_chatbot(
                user_id=userinfo["user"]["sub"],
                session_id=session_id,
                text=prompt,
                image_file=image_file,
                image_format=image_format,
            )
        )

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)


def get_chatbot_history(request: HttpRequest):
    userinfo = get_userinfo_context(request)

    if not userinfo["user"]:
        return JsonResponse({"error": "Error: User not logged in"}, status=403)

    data = request.GET

    try:
        session_id = data["session_id"]
    except KeyError:
        return JsonResponse({"error": "Error: Missing key prompt"}, status=400)

    messages = query_chat_history(user_id=userinfo["user"]["sub"], session_id=session_id)

    for message in messages:
        if "imageData" in message:
            message["imageURL"] = generate_presigned_url(message["imageData"])

    return JsonResponse({"data": messages})
