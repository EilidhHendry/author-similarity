from django.contrib import admin
from .models import Author, Text, Chunk, Classifier
from classifier import svm


class ChunkAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'text', 'author']
    list_filter = ['author', 'text']
    search_fields = ['author__name', 'text__name']


admin.site.register(Chunk, ChunkAdmin)


class ChunkInline(admin.StackedInline):
    model = Chunk


class TextAdmin(admin.ModelAdmin):
    actions = ['process_text', 'compute_average']
    list_display = ['__unicode__', 'author']
    list_filter = ['author']
    search_fields = ['name', 'author__name']

    def process_text(self, request, queryset):
        for selected_text in queryset:
            selected_text.delete()
            selected_text.save()

    def compute_average(self, request, queryset):
        for selected_text in queryset:
            selected_text.compute_own_average_chunk()


admin.site.register(Text, TextAdmin)


class TextInline(admin.StackedInline):
    model = Text


class AuthorAdmin(admin.ModelAdmin):
    actions = ['compute_average']
    search_fields = ['name']
    inlines = [
        TextInline,
    ]

    def compute_average(self, request, queryset):
        for selected_author in queryset:
            selected_author.compute_own_average_chunk()


admin.site.register(Author, AuthorAdmin)


class ClassifierAdmin(admin.ModelAdmin):
    actions = ['train_classifier', 'find_accuracy']
    list_display = ['__unicode__', 'status']

    def train_classifier(self, request, queryset):
        classifier = queryset[0]
        classifier.train()

    def find_accuracy(self, request, queryset):
        print "Fetching Chunks"
        chunks = Chunk.get_chunks()
        authors = []
        fingerprints = []
        for chunk in chunks:
            authors.append(chunk.author.name)
            fingerprints.append(chunk.get_fingerprint_list())
        mean = svm.find_classifier_accuracy(fingerprints, authors)
        print "Accuracy: ", mean


admin.site.register(Classifier, ClassifierAdmin)
