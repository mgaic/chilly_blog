from django.contrib import admin
from .models import CustomComment

# Register your models here.

@admin.register(CustomComment)
class CustomCommentAdmin(admin.ModelAdmin):
    list_filter = ('comment_blog', 'comment_user', 'comment_time',)
    list_display = ('id', 'comment_blog', 'comment_user', 'comment_time', 'short_content') #显示字段
    list_display_links = ('id', 'comment_blog', 'comment_user', 'comment_time', 'short_content') #点击可进入编辑界面
    # list_editable = ['update_time'] #可以编辑的字段


    def comment_blog(self, obj):
        return obj.comment_blog.title

    def comment_user(self, obj):
        return obj.comment_user.username

    def comment_content(self, obj):
        return obj.comment_content
