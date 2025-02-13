# Generated by Django 5.1.4 on 2025-01-17 14:05

import app_bibliothecaire.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_bibliothecaire', '0007_remove_cd_dateemprunt_remove_cd_emprunteur_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='date_emprunt',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='media',
            name='emprunteur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_bibliothecaire.membre'),
        ),
        migrations.CreateModel(
            name='Emprunt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_emprunt', models.DateTimeField(auto_now_add=True)),
                ('date_retour_prevue', models.DateField(default=app_bibliothecaire.models.get_default_loan_date)),
                ('date_retour_effective', models.DateField(blank=True, null=True)),
                ('emprunteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emprunts', to='app_bibliothecaire.membre')),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emprunts', to='app_bibliothecaire.media')),
            ],
        ),
    ]
