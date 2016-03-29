from django.apps import AppConfig

class SimilarityAppConfig(AppConfig):
	name = "similarity"
	verbose_name = "Similartiy app"
	run_ready = False

	def ready(self):
		if not self.run_ready:
			print "Checking for system classifier"
			from .models import Classifier
			has_classifier = Classifier.objects.all().exists()
			if has_classifier:
				print "Classifier exists"
			else:
				print "Creating system classifier"
				system_classifier = Classifier()
				system_classifier.save()
			self.run_ready = True
