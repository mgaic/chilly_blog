from django.contrib import admin
from .models import  Blog,BlogType
from django.core.cache import cache

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_filter = ('blog_type', 'update_time')
    list_display = ('id', 'title', 'blog_type', 'update_time', 'read_count') #显示字段
    list_display_links = ('id', 'title', 'blog_type', 'update_time', 'read_count') #点击可进入编辑界面
    # list_editable = ['update_time'] #可以编辑的字段

    def blog_type(self, obj):
        return obj.blog_type.type_name

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        print("save blog")
        if cache.get("hot_blogs"):
            cache.delete('hot_blogs')
            print("删除 hot_blogs cache")
        if cache.get("latest_blogs"):
            cache.delete('latest_blogs')
            print("删除 latest_blogs cache")
        if cache.get('date_count_dict'):
            cache.delete('date_count_dict')
            print("删除 date_count_dict cache")
        if cache.get('all_blogs'):
            cache.delete('all_blogs')
            print("删除 all_blogs cache")
。。


    def delete_model(self, request, obj):
        print("delete blog")
        if cache.get("hot_blogs"):
            cache.delete('hot_blogs')
            print("删除 hot_blogs cache")
        if cache.get("latest_blogs"):
            cache.delete('latest_blogs')
            print("删除 latest_blogs cache")
        if cache.get('date_count_dict'):
            cache.delete('date_count_dict')
            print("删除 date_count_dict cache")
        if cache.get('all_blogs'):
            cache.delete('all_blogs')
            print("删除 all_blogs cache")

        super().delete_model(request, obj)



@admin.register(BlogType)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name',)
    list_display_links = ('id', 'type_name',)

    def save_model(self, request, obj, form, change):

        if cache.get("blog_types"):
            cache.delete('blog_types')
            print("删除 blog_types cache")

        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):

        if cache.get("blog_types"):
            cache.delete('blog_types')
            print("删除 blog_types cache")

        super().delete_model(request, obj)
