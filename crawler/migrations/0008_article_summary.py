# Generated by Django 2.1.3 on 2018-12-04 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0007_articletopic'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='summary',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
