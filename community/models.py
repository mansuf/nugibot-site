import uuid
from django.db import models

# Create your models here.


def get_community_image_post_directory(instance, filename: str):
    # Get the file extension
    ext = filename.split(".")[-1]
    # Generate UUID for filename
    unique_filename = f"{uuid.uuid4()}.{ext}"
    # Return path with UUID filename
    return f"community_posts/{uuid.uuid4()}/{unique_filename}"


class CommunityPost(models.Model):
    parent = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    content_text = models.TextField()
    content_image = models.ImageField(
        upload_to=get_community_image_post_directory, default=None
    )
    likes = models.BigIntegerField()


class CommunityPostComment(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.DO_NOTHING)
    author = models.CharField(max_length=255)
    content_text = models.TextField()
    likes = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now=True)
