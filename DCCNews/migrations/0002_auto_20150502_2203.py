# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DCCNews', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='path',
        ),
        migrations.AddField(
            model_name='image',
            name='image',
            field=models.ImageField(default=b'', upload_to=b'images'),
        ),
    ]
