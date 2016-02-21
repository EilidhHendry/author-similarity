from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from models import Chunk


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
