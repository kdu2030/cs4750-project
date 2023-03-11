from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


# Create your views here.

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "hooeats_app/index.html")