# Generated by Django 3.2.4 on 2021-09-04 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enigmes', '0008_auto_20210902_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enigme',
            name='credits_image',
            field=models.TextField(blank=True, null=True, verbose_name="Crédits/Licence de l'image"),
        ),
    ]
