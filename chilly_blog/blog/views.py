import json
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from .models import Blog, BlogType
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.cache import cache

# 首页
def index(request):
    context = {}

    # 所有博客类型
    if cache.get("blog_types"): # 如果博客类型在缓存中，就从缓存中取得类型
        blog_types = cache.get("blog_types")
        print("从缓存中加载博客类型")
    else:                          #操作DB取博客类型,并且添加缓存
        blog_types = BlogType.objects.all()
        cache.set("blog_types", blog_types, 1800)
        print("添加博客类型缓存")

    # 时间排序所有博客
    if cache.get("all_blogs"):
        all_blogs = cache.get("all_blogs")
        print("从缓存中加载所有博客")
    else:
        all_blogs = Blog.objects.all().order_by('-update_time')
        cache.set("all_blogs", all_blogs, 1800)
        print("添加所有博客缓存")

    #分页
    paginator = Paginator(all_blogs, settings.INDEX_PAGE_BLOG_COUNT)
    page_num = request.GET.get('page', 1)  # 获取页码参数
    page_of_blogs = paginator.get_page(page_num) #按照时间排序分页后的博客
    current_page = page_of_blogs.number     #当前页码
    page_range = list(range(max(current_page - 2, 1), min(current_page + 3, page_of_blogs.paginator.num_pages)))
    if page_range[0] >= 3:
        page_range.insert(0, "...")
    if page_range[-1] <= page_of_blogs.paginator.num_pages - 2:
        page_range.append("...")
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != page_of_blogs.paginator.num_pages:
        page_range.append(page_of_blogs.paginator.num_pages)

    # 获取阅读量排序最近5篇博客
    if cache.get("hot_blogs"):
        hot_blogs = cache.get("hot_blogs")
        print("从缓存中加载热门博客")
    else:
        hot_blogs = Blog.objects.all().order_by('-read_count', '-update_time')[:5]
        cache.set("hot_blogs", hot_blogs, 1800)
        print("添加热门博客缓存")

    #获取更新时间排序最近5篇博客
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
            count = Blog.objects.filter(update_time__year=blog_date.year, update_time__month=blog_date.month).count()
            date_count_dict[blog_date] = count
        cache.set("date_count_dict", date_count_dict, 1800)
        print("添加最近更新日期分类以及数量")

    context['date_count_dict'] = date_count_dict
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = blog_types
    context['hot_blogs'] = hot_blogs
    context['latest_blogs'] = latest_blogs

    return render(request, 'blog/index.html', context)


# 博客详情
def detail(request, blog_id):
    context = {}
    # 当前博客
    cur_blog = get_object_or_404(Blog, id=blog_id)
    context['cur_blog'] = cur_blog

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


    context['previous_blog'] = Blog.objects.filter(id__lt=cur_blog.id).last()
    context['next_blog'] = Blog.objects.filter(id__gt=cur_blog.id).first()
    context['blog_types'] = blog_types
    context['hot_blogs'] = hot_blogs
    context['latest_blogs'] = latest_blogs
    context['date_count_dict'] = date_count_dict

    #判断cookie,进行博客计数
    if 'read' not in request.COOKIES:
        response = render(request, 'blog/detail.html', context)
        cur_blog.read_count += 1
        cur_blog.save()
        read_list = [blog_id]
        print(json.dumps(read_list))
        response.set_cookie("read", json.dumps(read_list), max_age=60 * 30)
        return response

    # read不在cookie中 判断文章id是否在已阅读文章中
    read_list = request.COOKIES['read']
    read_list = json.loads(read_list)
    response = render(request, 'blog/detail.html', context)
    if blog_id not in read_list:
        cur_blog.read_count += 1
        cur_blog.save()
        read_list.append(blog_id)
        response.set_cookie("read", json.dumps(read_list), max_age=60 * 30)

    return response


# 类型分类下的博客
def get_blog_by_type(request, type_id):
    context = {}

    blog_type =get_object_or_404(BlogType, id=type_id)
    blogs_with_type = blog_type.blog_set.all()

    #分页
    paginator = Paginator(blogs_with_type, settings.INDEX_PAGE_BLOG_COUNT)
    page_num = request.GET.get('page', 1)  # 获取页码参数
    page_of_blogs = paginator.get_page(page_num)  # 按照时间排序分页后的博客
    current_page = page_of_blogs.number  # 当前页码
    print('current_page', current_page)
    page_range = list(range(max(current_page - 2, 1), current_page)) + \
                 list(range(current_page, min(current_page + 2, paginator.num_pages) + 1))
    if page_range[0] >= 3:
        page_range.insert(0, "...")
    if page_range[-1] <= page_of_blogs.paginator.num_pages - 2:
        page_range.append("...")
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != page_of_blogs.paginator.num_pages:
        page_range.append(page_of_blogs.paginator.num_pages)

    context['page_of_blogs_with_type'] = page_of_blogs

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
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    print(page_range)

    return render(request, 'blog/type.html', context)

# 日期分类下的博客
def get_blog_by_date(request, year, month):
    context = {}
    blogs_with_date = Blog.objects.filter(update_time__year=year, update_time__month=month)

    #分页
    paginator = Paginator(blogs_with_date, settings.INDEX_PAGE_BLOG_COUNT)
    page_num = request.GET.get('page', 1)  # 获取页码参数
    page_of_blogs = paginator.get_page(page_num)  # 按照时间排序分页后的博客
    current_page = page_of_blogs.number  # 当前页码
    print('current_page', current_page)
    page_range = list(range(max(current_page - 2, 1), current_page)) + \
                 list(range(current_page, min(current_page + 2, paginator.num_pages) + 1))
    if page_range[0] >= 3:
        page_range.insert(0, "...")
    if page_range[-1] <= page_of_blogs.paginator.num_pages - 2:
        page_range.append("...")
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != page_of_blogs.paginator.num_pages:
        page_range.append(page_of_blogs.paginator.num_pages)
    context['page_of_blogs_with_date'] = page_of_blogs

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
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range

    return render(request, 'blog/date.html', context)
