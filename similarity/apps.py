from django.apps import AppConfig
from .models import Classifier

class SimilarityAppConfig(AppConfig):
	name = "similarity"
	verbose_name = "Similartiy app"
	def ready(self):
		print "Checking for system classifier"
		has_classifier = Classifier.objects.all().exists()
		if has_classifier:
			print "Classifier exists"
		else:
			print "Creating system classifier"
			system_classifier = Classifier()
			system_classifier.save()
