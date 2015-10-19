from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


def index(request):
    return render(request, 'similarity/base.html')
