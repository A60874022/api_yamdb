# Generated by Django 2.2.16 on 2022-11-20 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20221120_1511'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='Category',
        ),
        migrations.RenameModel(
            old_name='Genre',
            new_name='Genre',
        ),
        migrations.RenameModel(
            old_name='GenreTitles',
            new_name='GenreTitles',
        ),
        migrations.AlterField(
            model_name='titles',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Category', to='reviews.Category'),
        ),
    ]
