# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion_sam', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grade', models.FloatField()),
                ('materia', models.ForeignKey(to='configuracion_sam.Materia')),
                ('subperiodo', models.ForeignKey(to='configuracion_sam.Subperiodo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Grade_Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='grade',
            name='type',
            field=models.ForeignKey(to='academic_office_sam.Grade_Type'),
            preserve_default=True,
        ),
    ]
