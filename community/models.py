from django.db import models

# Create your models here.


def get_community_image_post_directory(instance, filename: str):
    return f"community_posts/{instance.id}/{filename}"


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
