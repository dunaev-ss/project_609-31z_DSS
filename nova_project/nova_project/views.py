from django.http import HttpResponse
from django.shortcuts import render


def homepage(request):
    # return HttpResponse('<h1>Home</h1>')
    return render(request, 'homepage.html')


def about(request):
    # return HttpResponse('<h1>About</h1>')
    return render(request, 'about.html')