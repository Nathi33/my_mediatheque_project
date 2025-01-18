# Generated by Django 5.1.4 on 2025-01-18 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_bibliothecaire', '0009_media_category'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PlateauDeJeu',
            new_name='Plateau',
        ),
        migrations.AlterField(
            model_name='media',
            name='category',
            field=models.CharField(choices=[('livre', 'Livre'), ('dvd', 'Dvd'), ('cd', 'Cd'), ('plateau', 'Plateau')], default='livre', max_length=10),
        ),
    ]
