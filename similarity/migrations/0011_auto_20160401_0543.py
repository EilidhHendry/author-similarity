# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('similarity', '0010_remove_chunk_chunk_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='average_chunk',
            field=models.ForeignKey(related_name='average_chunk_author', blank=True, to='similarity.Chunk', null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='average_chunk',
            field=models.ForeignKey(related_name='average_chunk_text', blank=True, to='similarity.Chunk', null=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='author',
            field=models.ForeignKey(blank=True, to='similarity.Author', null=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='text',
            field=models.ForeignKey(blank=True, to='similarity.Text', null=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='text_chunk_number',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
