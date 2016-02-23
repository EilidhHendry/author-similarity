# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('similarity', '0008_classifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classifier',
            name='status',
            field=models.CharField(default=b'untrained', max_length=10, choices=[(b'untrained', b'untrained'), (b'trained', b'trained'), (b'training', b'training')]),
        ),
    ]
