from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def login(request):
    if request.method == 'GET':

        return render(request, 'login/login.html')