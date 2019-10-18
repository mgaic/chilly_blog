from haystack.generic_views import SearchView
from blog.models import Blog

class MySearchView(SearchView):
    """My custom search view."""

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.all()

    def get_context_data(self, *args, **kwargs):

        context = super().get_context_data(*args, **kwargs)
        context['name'] = 'chilly'
        print(context)
        return  context

    # def extra_context(self):  # 重载extra_context来添加额外的context内容
    #     context = super().extra_context()
    #     # side_list = Topic.objects.filter(kind='major').order_by('add_date')[:8]
    #     context['behave'] = "love"
    #     print(context)
    #     return context


