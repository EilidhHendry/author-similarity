from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from models import Classifier

def index(request):
    return render(request, 'similarity/base.html')

@csrf_exempt
def classify(request):
    text = ""
    text_key = 'text'
    if text_key in request.POST:
        text = str(request.POST[text_key])
    if text_key in request.GET:
        text = str(request.GET[text_key])
    system_classifier = Classifier.objects.first()
    result = system_classifier.classify(text)
    response = JsonResponse(result)
    return response
