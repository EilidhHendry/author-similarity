from django.contrib import admin
from .models import Author, Text, Chunk

admin.site.register(Author)
admin.site.register(Text)
admin.site.register(Chunk)
