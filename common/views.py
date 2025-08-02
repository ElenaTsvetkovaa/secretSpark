from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'common/home.html')

def health_check(request):
    return HttpResponse("OK", status=200)
