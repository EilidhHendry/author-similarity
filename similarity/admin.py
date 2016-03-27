from django.contrib import admin
from .models import Author, Text, Chunk, Classifier
from classifier import svm

admin.site.register(Chunk)

class ChunkInline(admin.StackedInline):
    model = Chunk

class TextAdmin(admin.ModelAdmin):
    actions = ['process_text']
    def process_text(self, request, queryset):
        for selected_text in queryset:
            selected_text.delete()
            selected_text.save()

admin.site.register(Text, TextAdmin)

class TextInline(admin.StackedInline):
    model = Text

class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        TextInline,
    ]

admin.site.register(Author, AuthorAdmin)

class ClassifierAdmin(admin.ModelAdmin):
    actions = ['train_classifier', 'find_accuracy']
    def train_classifier(self, request, queryset):
        classifier = queryset[0]
        classifier.train()
    train_classifier.short_description = "Train Classifier"
    def find_accuracy(self, request, queryset):
        print "Fetching Chunks"
        chunks = Chunk.objects.all()
        authors = []
        fingerprints = []
        for chunk in chunks:
            authors.append(chunk.author.name)
            fingerprints.append(chunk.get_fingerprint_list())
        mean = svm.find_classifier_accuracy(fingerprints, authors)
        print "Accuracy: ", mean

admin.site.register(Classifier, ClassifierAdmin)
