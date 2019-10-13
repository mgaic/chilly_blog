from django.http import HttpResponse
from django.shortcuts import render
from .models import Blog, BlogType
from django.shortcuts import get_object_or_404


#首页
def index(request):
    context = {}
    # 所有博客类型
    blog_types = BlogType.objects.all()
    context['blog_types'] = blog_types

    # 时间排序最近5篇博客
    context['latest_blogs'] = Blog.objects.all().order_by('-update_time')[:5]

    # 阅读量排序最近5篇博客
    context['hot_blogs'] = Blog.objects.all().order_by('-read_count', '-update_time')[:5]

    # 博客按照时间分类 以及每个分类下的博客数量
    date_count_dict = {}
    blog_dates = Blog.objects.dates('update_time', 'month', order='DESC')
    for blog_date in blog_dates:
        count = Blog.objects.filter(update_time__year=blog_date.year, update_time__month=blog_date.month).count()
        date_count_dict[blog_date] = count
    context['date_count_dict'] = date_count_dict
    return render(request, 'blog/index.html', context)

#博客详情
def detail(request, blog_id):

    context = {}
    # 当前博客
    cur_blog = get_object_or_404(Blog, id=blog_id)
    context['cur_blog'] = cur_blog
    # 所有博客类型
    blog_types = BlogType.objects.all()
    context['blog_types'] = blog_types

    # 时间排序最近5篇博客
    context['latest_blogs'] = Blog.objects.all().order_by('-update_time')[:5]

    # 阅读量排序最近5篇博客
    context['hot_blogs'] = Blog.objects.all().order_by('-read_count', '-update_time')[:5]

    # 博客按照时间分类 以及每个分类下的博客数量
    date_count_dict = {}
    blog_dates = Blog.objects.dates('update_time', 'month', order='DESC')
    for blog_date in blog_dates:
        count = Blog.objects.filter(update_time__year=blog_date.year, update_time__month=blog_date.month).count()
        date_count_dict[blog_date] = count
    context['date_count_dict'] = date_count_dict

    #上下篇
    context['previous_blog'] = Blog.objects.filter(id__lt = cur_blog.id).last()
    context['next_blog'] = Blog.objects.filter(id__gt = cur_blog.id).first()



    return render(request, 'blog/detail.html', context)

#类型分类下的博客
def get_blog_by_type(request, type_id):
    context = {}
    blog_type = get_object_or_404(BlogType, id = type_id)
    blogs_with_type =  blog_type.blog_set.all()
    context['blogs_with_type'] = blogs_with_type
    # 所有博客类型
    blog_types = BlogType.objects.all()
    context['blog_types'] = blog_types

    # 时间排序最近5篇博客
    context['latest_blogs'] = Blog.objects.all().order_by('-update_time')[:5]

    # 阅读量排序最近5篇博客
    context['hot_blogs'] = Blog.objects.all().order_by('-read_count', '-update_time')[:5]

    # 博客按照时间分类 以及每个分类下的博客数量
    date_count_dict = {}
    blog_dates = Blog.objects.dates('update_time', 'month', order='DESC')
    for blog_date in blog_dates:
        count = Blog.objects.filter(update_time__year=blog_date.year, update_time__month=blog_date.month).count()
        date_count_dict[blog_date] = count
    context['date_count_dict'] = date_count_dict

    return render(request, 'blog/type.html', context)

#日期分类下的博客
def get_blog_by_date(request, year, month):
    context = {}
    blogs_with_date = Blog.objects.filter(update_time__year=year, update_time__month=month)
    context['blogs_with_date'] = blogs_with_date
    # 所有博客类型
    blog_types = BlogType.objects.all()
    context['blog_types'] = blog_types

    # 时间排序最近5篇博客
    context['latest_blogs'] = Blog.objects.all().order_by('-update_time')[:5]

    # 阅读量排序最近5篇博客
    context['hot_blogs'] = Blog.objects.all().order_by('-read_count', '-update_time')[:5]

    # 博客按照时间分类 以及每个分类下的博客数量
    date_count_dict = {}
    blog_dates = Blog.objects.dates('update_time', 'month', order='DESC')
    for blog_date in blog_dates:
        count = Blog.objects.filter(update_time__year=blog_date.year, update_time__month=blog_date.month).count()
        date_count_dict[blog_date] = count
    context['date_count_dict'] = date_count_dict

    return render(request, 'blog/date.html', context)
