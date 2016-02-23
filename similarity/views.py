from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from models import Chunk, Classifier


def index(request):
    return render(request, 'similarity/base.html')

def all_chunks(request):
    chunks = Chunk.objects.all()
    authors = []
    fingerprints = []
    for chunk in chunks:
        authors.append(chunk.author.name)
        fingerprints.append(chunks[0].get_fingerprint())
    result = {
        "authors": authors,
        "fingerprints": fingerprints,
    }
    response = JsonResponse(result)
    return response

def classify(request):
    text = ""
    text_key = 'text'
    if (text_key in request.POST):
        text = str(request.POST[text_key])
    if (text_key in request.GET):
        text = str(request.GET[text_key])

    system_classifier = Classifier.objects.first()
    result = {}
    results = system_classifier.classify(text)
    response = JsonResponse(results, safe=False)
    return response
