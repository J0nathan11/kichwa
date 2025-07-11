# Generated by Django 4.1.13 on 2025-06-06 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Modulos', '0009_aprender_colores'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aprender_Cuerpo_Humano',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen_cue', models.ImageField(blank=True, null=True, upload_to='imagenes_aprender_cuerpo_humano/')),
                ('palabra_cue', models.CharField(max_length=100)),
                ('audio_kichwa_cue', models.FileField(blank=True, null=True, upload_to='audios_kichwa_cuerpo_humano/')),
            ],
        ),
    ]
