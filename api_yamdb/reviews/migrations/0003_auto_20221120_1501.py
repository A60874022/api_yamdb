# Generated by Django 2.2.16 on 2022-11-20 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_titles_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titles',
            name='rating',
            field=models.IntegerField(null=True),
        ),
    ]
