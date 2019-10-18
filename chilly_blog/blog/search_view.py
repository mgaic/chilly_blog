from django.core.cache import cache
from haystack.generic_views import SearchView
from blog.models import Blog

from blog.models import BlogType


class MySearchView(SearchView):
    """My custom search view."""

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.all()

    def get_context_data(self, *args, **kwargs):

        context = super().get_context_data(*args, **kwargs)

        # 所有博客类型
        if cache.get("blog_types"):  # 如果博客类型在缓存中，就从缓存中取得类型
            blog_types = cache.get("blog_types")
            print("从缓存中加载博客类型")
        else:  # 操作DB取博客类型,并且添加缓存
            blog_types = BlogType.objects.all()
            cache.set("blog_types", blog_types, 1800)
            print("添加博客类型缓存")

        # 获取阅读量排序最近5篇博客
        if cache.get("hot_blogs"):
            hot_blogs = cache.get("hot_blogs")
            print("从缓存中加载热门博客")
        else:
            hot_blogs = Blog.objects.all().order_by('-read_count', '-update_time')[:5]
            cache.set("hot_blogs", hot_blogs, 1800)
            print("添加热门博客缓存")

        # 获取更新时间排序最近5篇博客
        if cache.get("latest_blogs"):
            latest_blogs = cache.get("latest_blogs")
            print("从缓存中加载最近博客")
        else:
            latest_blogs = Blog.objects.all().order_by('-update_time')[:5]
            cache.set("latest_blogs", latest_blogs, 1800)
            print("添加最近更新博客缓存")

        # 博客按照时间分类 以及每个分类下的博客数量
        if cache.get("date_count_dict"):
            date_count_dict = cache.get("date_count_dict")
            print("从缓存中加载日期分类以及数量")
        else:
            date_count_dict = {}
            blog_dates = Blog.objects.dates('update_time', 'month', order='DESC')
            for blog_date in blog_dates:
                count = Blog.objects.filter(update_time__year=blog_date.year,
                                            update_time__month=blog_date.month).count()
                date_count_dict[blog_date] = count
            cache.set("date_count_dict", date_count_dict, 1800)
            print("添加最近更新日期分类以及数量")

        context['blog_types'] = blog_types
        context['hot_blogs'] = hot_blogs
        context['latest_blogs'] = latest_blogs
        context['date_count_dict'] = date_count_dict


        print(context)
        return  context




