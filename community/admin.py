from django.contrib import admin
from community.models import CommunityPost, CommunityPostComment

# Register your models here.


class CommunityPostAdmin(admin.ModelAdmin):
    pass


class CommunityPostCommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(CommunityPost, CommunityPostAdmin)
admin.site.register(CommunityPostComment, CommunityPostCommentAdmin)
