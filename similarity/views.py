from similarity.classifier import clean_up

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from models import Chunk, Classifier
from forms import InputForm

def index(request):
    text = ""
    if request.method == 'POST':
        form = InputForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data.get('input_file'):
                input_file = form.cleaned_data.get('input_file')
                print type(input_file)
                text = input_file.read()
            elif form.cleaned_data.get('text'):
                text = form.cleaned_data.get('text')
            return classify_text(text)
    else:
        form = InputForm(initial={'text': 'text here'})
    return render(request, 'similarity/base.html', {'form': form})

def classify(request):
    text = ""
    text_key = 'text'
    if (text_key in request.POST):
        text = str(request.POST[text_key])
    if (text_key in request.GET):
        text = str(request.GET[text_key])
    return classify_text(text)

def classify_text(text):
    system_classifier = Classifier.objects.first()
    result = {}
    result = system_classifier.classify(text)
    response = JsonResponse(result)
    return response
