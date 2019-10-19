from django.conf import settings
from django.contrib import auth
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def login(request):
    if request.method == 'GET':
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
        return render(request, 'login/login.html')
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        # 验证用户名和密码，验证通过的话，返回user对象
        user = auth.authenticate(username = username, password = password)

        if user:

            # 验证成功 登陆
            auth.login(request, user)
            print("成功登陆")
            # print("session : ", request.session['login_from'])
            try:
                return HttpResponseRedirect(request.session['login_from'])
            except:
                return HttpResponseRedirect('/')
        else:
            print("用户名或密码错误")
            return render(request, 'login/login.html', {'err_msg':'用户名或密码错误'})

def quit_login(request):
    logout(request=request)

    return HttpResponseRedirect('/')
    # pass

# Create your views here.

