from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
# from django.utils import timezone
class BlogType(models.Model):
    type_name = models.CharField(max_length = 32, verbose_name = '文章类型')

    class Meta:
        verbose_name = "博文类型"
        verbose_name_plural = "博文类型"

    def __str__(self):
        return self.type_name




class Blog(models.Model):

    title = models.CharField(max_length = 100, verbose_name = '文章标题')
    content = RichTextField(verbose_name = '内容')
    blog_type = models.ForeignKey(BlogType, on_delete = models.CASCADE, verbose_name = '文章类型')
    update_time = models.DateTimeField(auto_now = True, verbose_name = '更新时间')
    read_count  = models.IntegerField(default = 0, verbose_name = '文章阅读数')

    class Meta:
        ordering = ('-update_time',)
        verbose_name = "博文"
        verbose_name_plural = "博文"

    def __str__(self):
        return self.title

