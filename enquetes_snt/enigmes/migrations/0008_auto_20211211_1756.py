# Generated by Django 3.2.4 on 2021-12-11 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enigmes', '0007_auto_20211117_1854'),
    ]

    operations = [
        migrations.AddField(
            model_name='enigme',
            name='commentaires',
            field=models.TextField(blank=True, null=True, verbose_name='commentaire'),
        ),
        migrations.AddField(
            model_name='enigme',
            name='reponse_libre',
            field=models.BooleanField(default=False, verbose_name='question à réponse libre'),
        ),
    ]