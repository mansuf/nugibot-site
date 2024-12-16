import boto3
import os
import json
import traceback
from django.http import HttpRequest, HttpResponse, StreamingHttpResponse
from utils.userinfo import get_userinfo_context

from botocore.exceptions import ClientError

aws_access_key_id = os.environ.get("AWS_BEDROCK_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_BEDROCK_SECRET_ACCESS_KEY")

model_name = "us.meta.llama3-2-11b-instruct-v1:0"

client = boto3.client(
    "bedrock-runtime",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name="us-east-1",
)
print(client)


def make_formatted_prompt(text):
    prompt = f"""
<|begin_of_text|><|start_header_id|>user<|end_header_id|>
{text}
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
"""
    return prompt


def get_prepared_request(text):
    data = {"prompt": make_formatted_prompt(text), "max_gen_len": 4096, "temperature": 0.5}

    return json.dumps(data)


def iter_response_chatbot(text):
    try:
        streaming_response = client.invoke_model_with_response_stream(
            modelId=model_name, body=get_prepared_request(text)
        )

        for event in streaming_response["body"]:
            chunk = json.loads(event["chunk"]["bytes"])
            if "generation" in chunk:
                yield chunk["generation"].encode()
    except (ClientError, Exception) as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        yield b"errorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr"


def get_chatbot_response(request: HttpRequest):
    userinfo = get_userinfo_context(request)

    if not userinfo["user"]:
        return HttpResponse("Error: User not logged in", status=403)

    if request.method != "POST":
        return HttpResponse("Error: Method not allowed", status=405)

    data = request.POST

    try:
        prompt = data["prompt"]
    except KeyError:
        return HttpResponse("Error: Missing key prompt", status=400)

    return StreamingHttpResponse(iter_response_chatbot(prompt))
