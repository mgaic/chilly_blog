from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import Context, Template

# Create your views here.
from blog.models import Blog
from custom_comment.models import CustomComment


def custom_comment(request):
    if request.method == 'POST':
        print(request.POST['blog_id'], request.POST['comment_content'], request.POST['user_id'])
        try:
            comment_user = User.objects.get(id = int(request.POST['user_id']))
            comment_blog = Blog.objects.get(id = int(request.POST['blog_id']))
            comment_content = request.POST['comment_content']
            custom_comment = CustomComment(comment_user = comment_user, comment_blog = comment_blog, comment_content = comment_content)
            custom_comment.save()
            print("success")
        except:
            return JsonResponse({"status": "failed", "msg": "comment parameter error"})

        html = """<li class="comment even thread-even depth-0" id="li-comment-6">
				<article id="comment-6" class="comment">
						<header class="comment-meta comment-author vcard">
						<img src="http://www.zfsphp.com/uploads/images//avatar/201909/1569501373.jpg" class="photo" height="44" width="44"/>
						    <cite class="fn">{{comment.comment_user.username}} </cite>
							<time datetime="">{{comment.comment_time}}</time>
						</header>
						<section class="comment-content comment" style="margin-bottom:10px;line-height:25px;">{{comment.comment_content}} </section>
				</article></li>"""

        t = Template(html)
        c = Context({'comment': custom_comment})
        return JsonResponse({"status": "success", "msg": "comment success", "html":t.render(c) })

    print("failed")
    return JsonResponse({"status":"failed", "msg":"request method error"})
