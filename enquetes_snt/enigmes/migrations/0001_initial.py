# Generated by Django 3.2.4 on 2021-10-22 15:35

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import enigmes.models
import enigmes.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Enigme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('date_modification', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date de modification')),
                ('theme', models.CharField(choices=[('NC', 'Non défini'), ('INT', 'Internet'), ('WEB', 'Le Web'), ('RS', 'Les réseaux sociaux'), ('DATA', 'Les données structurées et leur traitement'), ('LCM', 'Localisation, cartographie, mobilité'), ('IEOC', 'Informatique embarquée et objets connectés'), ('IMG', 'La photographie numérique'), ('PY', 'Python')], default='NC', max_length=4, verbose_name='thème')),
                ('enonce', models.TextField(verbose_name='énoncé')),
                ('reponse', models.CharField(max_length=100, verbose_name='réponse')),
                ('indication', models.TextField(blank=True, null=True, verbose_name='indication')),
                ('url_image', models.URLField(blank=True, null=True, verbose_name="URL de l'image d'illustration")),
                ('credits_image', models.TextField(blank=True, null=True, verbose_name="Crédits/Licence de l'image")),
                ('fichier', models.FileField(blank=True, upload_to=enigmes.models.Enigme.repertoire_auteur, validators=[enigmes.validators.FileValidator(content_types=('text/csv', 'application/vnd.oasis.opendocument.spreadsheet', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'text/x-python', 'text/html', 'text/css', 'text/plain', 'application/json', 'image/jpeg', 'image/png'), max_size=1024000)], verbose_name='Fichier en pièce jointe')),
                ('auteur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'énigme',
            },
        ),
        migrations.CreateModel(
            name='Enquete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='', max_length=100, verbose_name='description')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('indications', models.BooleanField(default=True, verbose_name='indications')),
                ('score', models.BooleanField(default=True, verbose_name='score')),
                ('correction', models.BooleanField(default=False, verbose_name='correction')),
                ('ordre_aleatoire', models.BooleanField(default=False, verbose_name='ordre aléatoire des énigmes')),
                ('cle', models.CharField(default='', max_length=200, verbose_name='clé')),
                ('code', models.CharField(default=enigmes.models.generer_code_enquete_unique, max_length=10, null=True, unique=True, verbose_name="code de l'enquête")),
                ('auteur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('enigmes', models.ManyToManyField(blank=True, related_name='enigmes', to='enigmes.Enigme')),
            ],
            options={
                'verbose_name': 'enquête',
            },
        ),
        migrations.CreateModel(
            name='Resultat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reponses', models.TextField(blank=True, null=True, verbose_name='réponses')),
                ('id_eleve', models.CharField(default='', max_length=100, validators=[django.core.validators.RegexValidator('^([a-zA-Z]?)[0-9\\-\\_]*', "L'identifiant saisi n'est pas valide. Veuillez consultez votre professeur.")], verbose_name='id_eleve')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('enquete', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='enquete', to='enigmes.enquete')),
            ],
            options={
                'verbose_name': 'résultat',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=enigmes.models.Image.repertoire_images_auteur, validators=[enigmes.validators.FileValidator(content_types=('image/jpeg', 'image/png'), max_size=307200)], verbose_name="Téléverser une image d'illustration")),
                ('auteur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Fichier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fichier', models.FileField(upload_to=enigmes.models.Fichier.repertoire_fichiers_auteur, validators=[enigmes.validators.FileValidator(content_types=('text/csv', 'application/vnd.oasis.opendocument.spreadsheet', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'text/x-python', 'text/html', 'text/css', 'text/plain', 'application/json', 'image/jpeg', 'image/png'), max_size=1024000)], verbose_name='Ajouter une pièce jointe')),
                ('auteur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='enigme',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='img', to='enigmes.image'),
        ),
    ]
