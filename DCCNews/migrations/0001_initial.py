# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(max_length=400)),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('frequency', models.IntegerField(default=50)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('init_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now_add=True)),
                ('modification_user_id', models.ForeignKey(related_name='modification_user', to=settings.AUTH_USER_MODEL)),
                ('priority_id', models.ForeignKey(to='DCCNews.Priority')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('view', models.CharField(max_length=400)),
                ('view_prev', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('number', models.IntegerField()),
                ('publication_id', models.ForeignKey(to='DCCNews.Publication')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='publication',
            name='tag_id',
            field=models.ForeignKey(to='DCCNews.Tag'),
        ),
        migrations.AddField(
            model_name='publication',
            name='template_id',
            field=models.ForeignKey(to='DCCNews.Template'),
        ),
        migrations.AddField(
            model_name='publication',
            name='type_id',
            field=models.ForeignKey(to='DCCNews.Type'),
        ),
        migrations.AddField(
            model_name='publication',
            name='user_id',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='image',
            name='publication_id',
            field=models.ForeignKey(to='DCCNews.Publication'),
        ),
    ]
