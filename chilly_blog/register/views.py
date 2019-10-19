from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
from django.urls import reverse
from celery_tasks.tasks import send_register_success_email

def register(request):
    if request.method == 'GET':
        print("GET")
        return render(request, 'register/register.html')

    if request.method == 'POST':
        # context = {}
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')

        try:
            print("1")
            user = User.objects.get(username=username)
            return render(request, 'register/register.html',  {'error_msg': '账号已经存在,换个账号试试吧!'})
        except:
            try:
                print(2)
                user = User.objects.get(email = email)
                return render(request, 'register/register.html',
                              {'error_msg': '邮箱已经存在,换个昵称试试吧!'})
            except:
                print("3")
                if password != password_confirmation:
                    return render(request, 'register/register.html',
                                  { 'error_msg': '两次密码输入不一致,请重新注册'})
                else:
                    print("4")

                    password = make_password(password, None, 'pbkdf2_sha256')
                    user = User(username=username, password=password, email=email)
                    user.save()
                    # ()
                    send_register_success_email.delay(email, user.username)

                    return HttpResponseRedirect( reverse('login') )

    return HttpResponse("123")
