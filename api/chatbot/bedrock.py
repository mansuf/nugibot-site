import boto3
import os
import traceback
import io
import requests
import json
import time
from PIL import Image
from botocore.exceptions import ClientError
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from .dynamodb import query_chat_history, add_chat_history
from .utils import handle_image_upload, generate_presigned_url

aws_access_key_id = os.environ.get("AWS_BEDROCK_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_BEDROCK_SECRET_ACCESS_KEY")

model_name = "us.meta.llama3-2-11b-instruct-v1:0"

client = boto3.client(
    "bedrock-runtime",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name="us-east-1",
)


def make_formatted_prompt(text):
    prompt = f"""
Jalankan prompt dibawah ini dengan konteks nutrisi dan gizi kesehatan makanan dan minuman untuk manusia,
Serta berikan saran dan sugesti setiap respon yang diberikan. Jika prompt tersebut tidak valid, 
maka tolak permintaan prompt tersebut dengan kata kata halus dan baik. Jika diberikan gambar berhubungan dengan makanan atau makanan,
maka analisis gambar tersebut sesuai dengan permintaan prompt yang dikasih

{text}
"""
    return prompt


def iter_response_chatbot(user_id, session_id, text, image_file, image_format):
    query_messages = query_chat_history(user_id, session_id)

    request_messages = []

    for message in query_messages:
        query_data = {}
        content = []
        query_data["role"] = message["role"]

        content.append({"text": message["message"]})

        if message.get("imageData"):
            image_url = generate_presigned_url(message["imageData"])
            image_data = requests.get(image_url).content
            content.append(
                {
                    "image": {
                        "format": message["imageFormat"],
                        "source": {"bytes": image_data},
                    }
                }
            )

        query_data["content"] = content

        request_messages.append(query_data)

    query_data = {}
    query_data["role"] = "user"
    content = []
    content.append({"text": make_formatted_prompt(text)})

    fp = io.BytesIO()
    if image_file:
        image_data = Image.open(image_file)
        image_data.save(fp, "png")
        content.append(
            {
                "image": {
                    "format": "png",
                    "source": {"bytes": fp.getvalue()},
                }
            }
        )

        fp = io.BytesIO(fp.getvalue())
        fp.name = image_file.name
        fp.content_type = image_file.content_type

    query_data["content"] = content
    request_messages.append(query_data)

    try:
        request_body = {
            "inferenceConfig": {
                "maxTokens": 4096,
                "temperature": 0.5,
            },
            "messages": request_messages,
        }

        streaming_response = client.converse_stream(modelId=model_name, **request_body)

        response_text = ""
        for event in streaming_response["stream"]:
            if "contentBlockDelta" not in event:
                continue

            chunk = event["contentBlockDelta"]["delta"]["text"]
            yield chunk.encode()

            response_text += chunk

        add_chat_history(
            user_id,
            session_id,
            "user",
            text,
            "" if not image_file else handle_image_upload(fp, user_id),
            "png",
        )
        add_chat_history(user_id, session_id, "assistant", response_text, "", "")

    except (ClientError, Exception) as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        yield b"errorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr"


def generate_bedrock_calorie_recommendations_response(metrics):
    prompts = {
        "daily_total": f"Given the user's daily calorie intake is {metrics['calories_day']} kcal, provide a detailed recommendation for their Total Daily Calorie Recommendations in 2-3 sentences.",
        "monthly_total": f"Based on the monthly calorie intake of {metrics['calories_month']} kcal, provide specific recommendations for Monthly Total Calorie Recommendation in 2-3 sentences.",
        "daily_limit": f"Considering the current daily intake of {metrics['calories_day']} kcal, suggest a Recommended Daily Calorie Limit and explain why in 2-3 sentences.",
        "monthly_limit": f"Looking at the monthly consumption of {metrics['calories_month']} kcal, provide a Recommended Monthly Calorie Limit with explanation in 2-3 sentences.",
    }

    for key, prompt in prompts.items():
        t = f"""
<|begin_of_text|><|start_header_id|>user<|end_header_id|>
{prompt}
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
        """

        body = {"prompt": t, "max_gen_len": 4096, "temperature": 0.5}

        response = client.invoke_model(modelId=model_name, body=json.dumps(body))

        response_body = json.loads(response["body"].read())
        yield f"data: {json.dumps({'type': key, 'content': response_body['generation']})}\n\n"
        time.sleep(0.1)  # Small delay between responses


def generate_calorie_recommendations(request):
    from food_track.views import calculate_calorie_metrics

    # Calculate metrics first
    metrics = calculate_calorie_metrics(request, raw=True)

    response = StreamingHttpResponse(
        generate_bedrock_calorie_recommendations_response(metrics),
        content_type="text/event-stream",
    )
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response


@require_http_methods(["POST"])
def get_recommendations_based_on_medical_history(request):
    try:
        data = json.loads(request.body)
        medical_history = data.get("medical_history", "")

        prompt = f"""
<|begin_of_text|><|start_header_id|>user<|end_header_id|>
Based on the medical condition: {medical_history}, 
provide two lists:
1. Recommended physical activities that are safe and beneficial
2. Recommended diet plans and foods

Format the response as JSON with two arrays: 'activities' and 'diet',
and please inside the activities and diet keys in the JSON response, make sure it's only list response
not another object or dict
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
        """

        response = client.invoke_model(
            modelId=model_name,
            body=json.dumps(
                {
                    "prompt": prompt,
                    "max_gen_len": 4096,
                    "temperature": 0.5,
                }
            ),
        )

        response_body = json.loads(response["body"].read())

        try:
            recommendations = json.loads(response_body["generation"])
        except Exception:
            recommendations = {
                "activities": ["No specific activities found"],
                "diet": ["No specific diet recommendations found"],
            }

        return JsonResponse(recommendations)

    except Exception as e:
        return JsonResponse(
            {
                "error": str(e),
                "activities": ["Error getting recommendations"],
                "diet": ["Error getting recommendations"],
            },
            status=500,
        )
