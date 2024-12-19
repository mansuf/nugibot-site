import boto3
import os
import uuid
import pytz
from datetime import datetime, timezone
from botocore.exceptions import ClientError

aws_access_key_id = os.environ.get("AWS_DYNAMODB_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_DYNAMODB_SECRET_ACCESS_KEY")

dynamodb = boto3.client(
    "dynamodb",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name="ap-southeast-1",
)


def add_chat_history(
    user_id,
    session_id,
    role,
    message,
    image_data=None,
    image_format=None,  # Added image_format parameter
):
    """
    Add chat history data to DynamoDB table using boto3.client with UUID v4 as messageId

    Parameters:
    user_id (str): User ID
    session_id (str): Session ID
    role (str): Role of the message sender
    message (str): The message content
    image_data (str): Base64 encoded image data (optional)
    image_format (str): Format of the image (optional, e.g., 'png', 'jpeg')

    Returns:
    bool: True if successful, False if failed
    str: message_id if successful, None if failed
    """
    try:
        while True:  # Keep trying until successful
            # Generate a new UUID v4
            message_id = str(uuid.uuid4())

            # Get current timestamp in ISO format
            timestamp = datetime.now(tz=timezone.utc).isoformat()

            # Prepare item data
            item = {
                "messageId": {"S": message_id},
                "userId": {"S": user_id},
                "sessionId": {"S": session_id},
                "role": {"S": role},
                "message": {"S": message},
                "createdAt": {"S": timestamp},
            }

            # Add image_data and image_format if provided
            if image_data:
                item["imageData"] = {"S": image_data}
            if image_format:
                item["imageFormat"] = {"S": image_format}

            try:
                # Try to put item with a condition that the messageId doesn't exist
                dynamodb.put_item(
                    TableName="NugibotChatHistory",
                    Item=item,
                    ConditionExpression="attribute_not_exists(messageId)",
                )

                # If we reach here, the put was successful
                print(
                    f"Successfully added chat history for user {user_id}, session {session_id}, messageId {message_id}"
                )
                return True, message_id

            except ClientError as e:
                if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                    # UUID collision occurred (extremely unlikely), continue the loop to try again
                    print("UUID collision occurred, retrying with new UUID...")
                    continue
                else:
                    # Some other error occurred
                    raise e

    except ClientError as e:
        print(f"Error adding chat history: {e.response['Error']['Message']}")
        return False, None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False, None


def query_chat_history(user_id: str, session_id: str):
    """
    Query chat history from DynamoDB table filtering by userId and sessionId using boto3.client

    Parameters:
    user_id (str): User ID to query for
    session_id (str): Session ID to filter by

    Returns:
    list: List of items matching the query
    """
    try:
        # Scan parameters
        response = dynamodb.scan(
            TableName="NugibotChatHistory",
            FilterExpression="userId = :uid AND sessionId = :sid",
            ExpressionAttributeValues={
                ":uid": {"S": user_id},
                ":sid": {"S": session_id},
            },
        )

        # Convert DynamoDB format to regular Python dict
        items = []
        for item in response.get("Items", []):
            converted_item = {
                "messageId": item["messageId"]["S"],
                "userId": item["userId"]["S"],
                "sessionId": item["sessionId"]["S"],
                "role": item["role"]["S"],
                "message": item["message"]["S"],
                "createdAt": item["createdAt"]["S"],
            }
            if "imageData" in item:
                converted_item["imageData"] = item["imageData"]["S"]
            if "imageFormat" in item:
                converted_item["imageFormat"] = item["imageFormat"]["S"]
            items.append(converted_item)

        # Sort items by createdAt timestamp
        items.sort(key=lambda x: x["createdAt"])
        return items

    except ClientError as e:
        print(f"Error querying chat history: {e.response['Error']['Message']}")
        return []
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return []


def get_user_sessions(user_id: str):
    """
    Query list of unique sessionIds for a given userId from DynamoDB table.

    Parameters:
    user_id (str): User ID to query for

    Returns:
    list: List of dictionaries containing sessionId and latest message timestamp
    """
    try:
        # Scan parameters
        response = dynamodb.scan(
            TableName="NugibotChatHistory",
            FilterExpression="userId = :uid",
            ExpressionAttributeValues={
                ":uid": {"S": user_id},
            },
            ProjectionExpression="sessionId, createdAt",
        )

        # Process the response to get unique sessions with their latest timestamp
        sessions = {}
        for item in response.get("Items", []):
            session_id = item["sessionId"]["S"]
            timestamp = item["createdAt"]["S"]

            # Update session if this timestamp is more recent
            if (
                session_id not in sessions
                or timestamp > sessions[session_id]["lastMessageAt"]
            ):
                sessions[session_id] = {"sessionId": session_id, "lastMessageAt": timestamp}

        # Convert to list and sort by timestamp (most recent first)
        session_list = list(sessions.values())
        session_list.sort(key=lambda x: x["lastMessageAt"], reverse=True)

        return session_list

    except ClientError as e:
        print(f"Error querying user sessions: {e.response['Error']['Message']}")
        return []
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return []


def get_relative_time(timestamp_str):
    """
    Convert ISO timestamp to relative time (e.g., "2 hours ago")

    Parameters:
    timestamp_str (str): ISO format timestamp string

    Returns:
    str: Human readable relative time
    """
    try:
        # Parse the ISO timestamp
        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        now = datetime.now(pytz.UTC)
        diff = now - timestamp

        # Calculate the time difference
        seconds = diff.total_seconds()

        if seconds < 60:
            return "just now"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif seconds < 2592000:  # 30 days
            days = int(seconds / 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
        elif seconds < 31536000:  # 365 days
            months = int(seconds / 2592000)
            return f"{months} month{'s' if months != 1 else ''} ago"
        else:
            years = int(seconds / 31536000)
            return f"{years} year{'s' if years != 1 else ''} ago"
    except Exception as e:
        print(f"Error converting timestamp: {str(e)}")
        return timestamp_str


def truncate_message(message, max_length=50):
    """
    Truncate message to specified length and add ellipsis if necessary

    Parameters:
    message (str): Message to truncate
    max_length (int): Maximum length of the truncated message

    Returns:
    str: Truncated message
    """
    if len(message) <= max_length:
        return message
    return message[:max_length] + "..."


def query_all_chat_history_formatted(user_id: str):
    """
    Query all chat history from DynamoDB table for a specific user,
    organized by sessions with only the latest conversation pair

    Parameters:
    user_id (str): User ID to query for

    Returns:
    dict: Dictionary of sessions, each containing the latest conversation pair
    """
    try:
        # Scan parameters
        response = dynamodb.scan(
            TableName="NugibotChatHistory",
            FilterExpression="userId = :uid",
            ExpressionAttributeValues={
                ":uid": {"S": user_id},
            },
        )

        # Group items by session_id first
        sessions = {}

        # Sort all items by timestamp first
        sorted_items = sorted(response.get("Items", []), key=lambda x: x["createdAt"]["S"])

        for item in sorted_items:
            session_id = item["sessionId"]["S"]
            current_role = item["role"]["S"]

            # Initialize session if not exists
            if session_id not in sessions:
                sessions[session_id] = {
                    "sessionId": session_id,
                    "lastMessageAt": item["createdAt"]["S"],
                    "conversation": None,
                    "temp_dict": None,
                }

            converted_message = {
                "messageId": item["messageId"]["S"],
                "message": truncate_message(item["message"]["S"], max_length=50),
                "fullMessage": item["message"]["S"],
                "createdAt": get_relative_time(item["createdAt"]["S"]),
                "timestamp": item["createdAt"]["S"],
            }

            # Add image data if present
            if "imageData" in item:
                converted_message["imageData"] = item["imageData"]["S"]
            if "imageFormat" in item:
                converted_message["imageFormat"] = item["imageFormat"]["S"]

            if current_role == "user":
                # Start a new conversation pair
                sessions[session_id]["temp_dict"] = {
                    "user": converted_message,
                    "assistant": None,
                }
            elif current_role == "assistant":
                # Complete the conversation pair if there's a pending user message
                if sessions[session_id]["temp_dict"] is not None:
                    sessions[session_id]["temp_dict"]["assistant"] = converted_message
                    sessions[session_id]["conversation"] = sessions[session_id]["temp_dict"]
                    sessions[session_id]["temp_dict"] = None

            # Update last message timestamp
            if item["createdAt"]["S"] > sessions[session_id]["lastMessageAt"]:
                sessions[session_id]["lastMessageAt"] = item["createdAt"]["S"]

        # Handle any remaining unpaired user messages
        for session in sessions.values():
            if session["temp_dict"] is not None:
                session["conversation"] = session["temp_dict"]
            del session["temp_dict"]  # Remove temporary dictionary

        # Convert sessions to list and sort by last message timestamp (most recent first)
        sessions_list = list(sessions.values())
        sessions_list.sort(key=lambda x: x["lastMessageAt"], reverse=True)

        return sessions_list

    except ClientError as e:
        print(f"Error querying chat history: {e.response['Error']['Message']}")
        return []
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return []
