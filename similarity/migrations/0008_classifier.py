# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('similarity', '0007_auto_20160222_0106'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_trained', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=10, choices=[(b'untrained', b'untrained'), (b'trained', b'trained'), (b'training', b'training')])),
            ],
        ),
    ]
