from django.shortcuts import render

def home(request):
    return render(request, 'common/home.html')


def index(request):
    return render(request, 'common/home.html')

