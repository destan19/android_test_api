from django.shortcuts import render
from django.http import HttpResponse


def echo(request):
        return HttpResponse("echo...");
# Create your views here.
