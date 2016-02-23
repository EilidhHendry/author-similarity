from django.contrib import admin
from .models import Author, Text, Chunk, Classifier

admin.site.register(Author)
admin.site.register(Text)
admin.site.register(Chunk)

class ClassifierAdmin(admin.ModelAdmin):
    actions = ['train_classifier']
    def train_classifier(self, request, queryset):
        classifier = queryset[0]
        classifier.train()
    train_classifier.short_description = "Train Classifier"

admin.site.register(Classifier, ClassifierAdmin)
