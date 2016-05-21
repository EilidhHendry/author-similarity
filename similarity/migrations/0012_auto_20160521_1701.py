# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('similarity', '0011_auto_20160401_0543'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='status',
            field=models.CharField(default=b'updated', max_length=10, choices=[(b'updated', b'updated'), (b'outdated', b'outdated')]),
        ),
        migrations.AlterField(
            model_name='author',
            name='average_chunk',
            field=models.ForeignKey(related_name='average_chunk_author', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='similarity.Chunk', null=True),
        ),
        migrations.AlterField(
            model_name='text',
            name='average_chunk',
            field=models.ForeignKey(related_name='average_chunk_text', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='similarity.Chunk', null=True),
        ),
    ]
