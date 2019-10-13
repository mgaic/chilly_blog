from django.urls import path

from . import views

urlpatterns = [
    path('detail/<int:blog_id>', views.detail, name = "detail" ),
    path('type/<int:type_id>', views.get_blog_by_type, name = "type" ),
    path('dete/<int:year>/<int:month>', views.get_blog_by_date, name = "date" ),
]
