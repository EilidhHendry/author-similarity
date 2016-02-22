# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('similarity', '0006_auto_20160221_1052'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chunk',
            old_name='PRP_dollar_pos_relative_frequency',
            new_name='PRP_possessive_pos_relative_frequency',
        ),
        migrations.RenameField(
            model_name='chunk',
            old_name='WP_dollar_pos_relative_frequency',
            new_name='WP_possessive_pos_relative_frequency',
        ),
    ]
