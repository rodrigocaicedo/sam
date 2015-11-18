# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion_sam', '__first__'),
        ('academic_office_sam', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student_Grade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grade', models.FloatField()),
                ('assignment', models.ForeignKey(to='academic_office_sam.Grade')),
                ('student', models.ForeignKey(to='configuracion_sam.Matricula')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='grade',
            name='grade',
        ),
        migrations.RemoveField(
            model_name='grade',
            name='subperiodo',
        ),
        migrations.AddField(
            model_name='grade',
            name='parcial',
            field=models.ForeignKey(default=123, to='configuracion_sam.Estructura_Subperiodo'),
            preserve_default=False,
        ),
    ]
