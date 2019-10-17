from ckeditor.fields import RichTextField
from django.core.cache import cache
from django.db import models
# Create your models here.
# from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver


class BlogType(models.Model):
    type_name = models.CharField(max_length = 32, verbose_name = '文章类型')

    class Meta:
        verbose_name = "博文类型"
        verbose_name_plural = "博文类型"

    def get_blog_count(self):
        return self.blog_

    def __str__(self):
        return self.type_name




class Blog(models.Model):

    title = models.CharField(max_length = 100, verbose_name = '文章标题')
    content = RichTextField(verbose_name = '内容')
    blog_type = models.ForeignKey(BlogType, on_delete = models.CASCADE, verbose_name = '文章类型')
    update_time = models.DateTimeField( verbose_name = '更新时间')
    read_count  = models.IntegerField(default = 0, verbose_name = '文章阅读数')

    class Meta:
        ordering = ('-update_time',)
        verbose_name = "博文"
        verbose_name_plural = "博文"

    def __str__(self):
        return self.title

@receiver(post_delete, sender=Blog)
def delete_blog_cache(sender, instance, **kwargs):
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

@receiver(post_delete, sender=BlogType)
def delete_blogtype_cache(sender, instance, **kwargs):
    print("delete blogtype")
    if cache.get("blog_types"):
        cache.delete('blog_types')
        print("删除 blog_types cache")
