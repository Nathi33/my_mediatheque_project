# Generated by Django 5.1.4 on 2025-01-18 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_bibliothecaire', '0008_media_date_emprunt_media_emprunteur_emprunt'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='category',
            field=models.CharField(choices=[('livre', 'Livre'), ('dvd', 'Dvd'), ('cd', 'Cd')], default='livre', max_length=10),
        ),
    ]
