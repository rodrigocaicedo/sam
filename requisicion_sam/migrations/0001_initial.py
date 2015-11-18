# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion_sam', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item_Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.CharField(max_length=20)),
                ('cantidad', models.PositiveSmallIntegerField()),
                ('presentacion', models.CharField(max_length=1)),
                ('detalle', models.TextField()),
                ('descripcion_uso', models.TextField()),
                ('revisado', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Requisicion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('carga_horario', models.ForeignKey(to='configuracion_sam.Periodo_Lectivo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='item_request',
            name='Requisicion',
            field=models.ForeignKey(to='requisicion_sam.Requisicion'),
            preserve_default=True,
        ),
    ]
