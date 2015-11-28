# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import similarity.models


class Migration(migrations.Migration):

    dependencies = [
        ('similarity', '0003_auto_20151128_0602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chunk',
            name='chunk_file',
            field=models.FileField(default=None, null=True, upload_to=similarity.models.create_chunk_upload_path, blank=True),
        ),
        migrations.AlterField(
            model_name='text',
            name='text_file',
            field=models.FileField(default=None, null=True, upload_to=similarity.models.create_text_upload_path, blank=True),
        ),
    ]
