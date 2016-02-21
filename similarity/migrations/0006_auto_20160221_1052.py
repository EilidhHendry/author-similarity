# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('similarity', '0005_chunk_avg_word_length_syllables'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chunk',
            name='ampersand_relative_frequency',
        ),
        migrations.AddField(
            model_name='chunk',
            name='PRP_dollar_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='chunk',
            name='WP_dollar_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
