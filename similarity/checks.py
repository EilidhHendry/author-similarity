from django.core.checks import register
from .models import Classifier

@register()
def classifier_check(app_configs, **kwargs):
    errors = []
    print "Running classifier check"
    has_classifier = Classifier.objects.all().exists()
    if has_classifier:
        print "Classifier exists"
    else:
        print "Creating system classifier"
        system_classifier = Classifier()
        system_classifier.save()
    return errors
