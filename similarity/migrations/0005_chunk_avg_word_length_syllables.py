# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('similarity', '0004_auto_20151128_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='chunk',
            name='avg_word_length_syllables',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
