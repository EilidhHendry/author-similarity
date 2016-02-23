from django.contrib import admin
from .models import Author, Text, Chunk, Classifier

admin.site.register(Chunk)

class ChunkInline(admin.StackedInline):
    model = Chunk

class TextAdmin(admin.ModelAdmin):
    inlines = [
        ChunkInline,
    ]

admin.site.register(Text, TextAdmin)

class TextInline(admin.StackedInline):
    model = Text

class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        TextInline,
    ]

admin.site.register(Author, AuthorAdmin)

class ClassifierAdmin(admin.ModelAdmin):
    actions = ['train_classifier']
    def train_classifier(self, request, queryset):
        classifier = queryset[0]
        classifier.train()
    train_classifier.short_description = "Train Classifier"

admin.site.register(Classifier, ClassifierAdmin)
