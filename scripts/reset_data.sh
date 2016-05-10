#!/bin/bash
./venv/bin/python manage.py flush --noinput;
rm -rf ./similarity/classifier/data/texts/*;
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'admin')" | ./venv/bin/python manage.py shell;
