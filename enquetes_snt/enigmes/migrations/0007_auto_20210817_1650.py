# Generated by Django 3.2.4 on 2021-08-17 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enigmes', '0006_alter_enigme_fichier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enquete',
            name='cle',
            field=models.CharField(default='', max_length=200, verbose_name='clé'),
        ),
        migrations.AlterField(
            model_name='enquete',
            name='description',
            field=models.CharField(default='', max_length=100, verbose_name='description'),
        ),
    ]
