# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('requisicion_sam', '0002_auto_20151108_1559'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requisicion',
            old_name='periodo_lectivo',
            new_name='profesor',
        ),
    ]
