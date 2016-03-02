# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('similarity', '0009_auto_20160223_0849'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chunk',
            name='chunk_file',
        ),
    ]
