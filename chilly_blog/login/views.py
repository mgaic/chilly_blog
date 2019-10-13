from django.contrib import auth
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'login/login.html')
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        # 验证用户名和密码，验证通过的话，返回user对象
        user = auth.authenticate(username = username, password = password)

        if user:
            print("2")
            # 验证成功 登陆
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            print("用户名或密码错误")
            return render(request, 'login/login.html', {'err_msg':'用户名或密码错误'})

def quit_login(request):
    logout(request=request)

    return HttpResponseRedirect('/')
    # pass