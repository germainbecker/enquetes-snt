# Generated by Django 3.2.4 on 2021-10-23 17:39

from django.db import migrations, models
import django.db.models.deletion
import enigmes.models
import enigmes.validators


class Migration(migrations.Migration):

    dependencies = [
        ('enigmes', '0002_alter_enigme_fichier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enigme',
            name='credits_image',
            field=models.TextField(blank=True, null=True, verbose_name="Crédits de l'image"),
        ),
        migrations.AlterField(
            model_name='enigme',
            name='fichier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='enigme', to='enigmes.fichier'),
        ),
        migrations.AlterField(
            model_name='enigme',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='enigme', to='enigmes.image'),
        ),
        migrations.AlterField(
            model_name='fichier',
            name='fichier',
            field=models.FileField(upload_to=enigmes.models.Fichier.repertoire_fichiers_auteur, validators=[enigmes.validators.FileValidator(content_types=('text/csv', 'application/vnd.oasis.opendocument.spreadsheet', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'text/x-python', 'text/html', 'text/css', 'text/plain', 'application/json', 'image/jpeg', 'image/png'), max_size=1024000)], verbose_name='Sélectionner un fichier'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=enigmes.models.Image.repertoire_images_auteur, validators=[enigmes.validators.FileValidator(content_types=('image/jpeg', 'image/png'), max_size=307200)], verbose_name='Sélectionner une image'),
        ),
    ]
