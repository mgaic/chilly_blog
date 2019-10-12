from django.http import HttpResponse
from django.shortcuts import render
from .models import  Blog, BlogType
# Create your views here.
def index(request):
    context = {}
    blog_types = BlogType.objects.all()
    context['blog_types'] = blog_types
    context['latest_blogs'] = Blog.objects.all().order_by('-update_time')[:5]
    context['hot_blogs'] = Blog.objects.all().order_by('-read_count','-update_time')[:5]
    return render(request, 'blog/index.html', context)