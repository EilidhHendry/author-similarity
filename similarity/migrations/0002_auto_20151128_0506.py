# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('similarity', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chunk',
            name='chunk_file_path',
        ),
        migrations.AddField(
            model_name='chunk',
            name='chunk_file',
            field=models.FileField(default=None, null=True, upload_to=b'', blank=True),
        ),
        migrations.AddField(
            model_name='text',
            name='text_file',
            field=models.FileField(default=None, null=True, upload_to=b'', blank=True),
        ),
    ]
