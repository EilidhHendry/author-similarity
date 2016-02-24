from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from models import Chunk, Classifier
from forms import InputForm


def index(request):
    input_file=""
    #TODO: work with files
    if request.method == 'POST':
        form = InputForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['input_file']:
                input_file = uploaded_file(form.cleaned_data.get('input_file'))
            return classify(request)
    else:
        form = InputForm(initial={'text': 'text here'})
    return render(request, 'similarity/base.html', {'form': form})

def uploaded_file(request):
    with open(f) as input_file:
        for chunk in f.chunks():
            input_file.write(chunk)
    return input_file

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
    results.append(text)
    response = JsonResponse(results, safe=False)
    return response
