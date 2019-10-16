from django.contrib.auth.models import User
from django.db import models
from blog.models import Blog

# Create your models here.
# from chilly_blog.blog.models import Blog


class CustomComment(models.Model):
    comment_blog = models.ForeignKey(Blog, on_delete = models.CASCADE, verbose_name = "评论博客")
    comment_time = models.DateTimeField(auto_now = True, verbose_name = '评论时间' )
    comment_user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "评论用户" )
    comment_content = models.TextField(verbose_name = "内容简要")

    class Meta:
        ordering = ('-comment_time',)
        verbose_name = "评论"
        verbose_name_plural = "评论"

    def __str__(self):
        return self.comment_content[:50]

    def short_content(self):     #自定义显示的内容 配合admin
        if len(str(self.comment_content)) > 50:
            return '{}...'.format(str(self.comment_content)[0:50])
        else:
            return str(self.comment_content)

    # short_content.allow_tags = True
    short_content.short_description = u"评论内容"  #设置列名

