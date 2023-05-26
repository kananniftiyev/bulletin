from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def index(request):
    author_is_authenticated = False
    if author_is_authenticated:
        return render(request, 'app_news/main.html', context={'author_is_authenticated' : True})
    else:
        return render(request, 'app_news/main.html', context={'author_is_authenticated' : False})
    

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        author = authenticate(request, username=username, password=password)
        if author is not None:
            login(request, author)
            return redirect('index')
        else:
            return render(request, 'app_news/login.html', context={'error_message' : 'Invalid login'})

    else:
        return render(request, 'app_news/login.html')

                

