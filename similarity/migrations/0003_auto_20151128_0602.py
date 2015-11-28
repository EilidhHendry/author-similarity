# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('similarity', '0002_auto_20151128_0506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chunk',
            name='CC_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='CD_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='DT_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='EX_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='FW_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='IN_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='JJR_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='JJS_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='JJ_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='LS_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='MD_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='NNPS_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='NNP_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='NNS_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='NN_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='PDT_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='POS_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='PRP_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='RBR_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='RBS_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='RB_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='RP_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='TO_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='UH_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='VBD_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='VBG_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='VBN_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='VBP_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='VBZ_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='VB_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='WDT_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='WP_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='WRB_pos_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='a_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='about_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='after_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='against_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='all_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='ampersand_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='an_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='and_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='another_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='any_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='around_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='as_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='at_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='avg_sentence_length',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='avg_word_length',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='because_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='before_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='between_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='both_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='but_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='by_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='can_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='could_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='de_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='down_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='each_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='for_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='from_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='he_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='her_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='him_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='himself_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='his_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='i_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='if_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='in_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='into_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='it_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='its_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='lexical_diversity',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='like_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='may_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='me_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='might_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='must_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='my_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='myself_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='no_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='of_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='off_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='on_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='or_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='our_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='out_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='over_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='percentage_punctuation',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='shall_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='she_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='should_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='since_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='some_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='than_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='that_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='the_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='their_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='them_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='these_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='they_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='this_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='those_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='through_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='to_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='toward_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='under_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='until_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='up_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='us_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='we_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='what_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='which_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='who_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='will_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='with_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='within_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='would_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='you_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='your_relative_frequency',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
