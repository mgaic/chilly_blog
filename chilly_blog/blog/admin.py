from django.contrib import admin
from .models import  Blog,BlogType

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_filter = ('blog_type', 'update_time')
    list_display = ('id', 'title', 'blog_type', 'update_time', 'read_count') #显示字段
    list_display_links = ('id', 'title', 'blog_type', 'update_time', 'read_count') #点击可进入编辑界面
    # list_editable = ['update_time'] #可以编辑的字段

    def blog_type(self, obj):
        return obj.blog_type.type_name

@admin.register(BlogType)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name',)
    list_display_links = ('id', 'type_name',)
