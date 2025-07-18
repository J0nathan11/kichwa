# Generated by Django 4.1.13 on 2025-06-10 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Modulos', '0015_profesor_foto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo_eva', models.CharField(max_length=200)),
                ('descripcion_eva', models.TextField()),
                ('estado_eva', models.BooleanField(default=True)),
                ('tipo_aprendizaje_eva', models.TextField()),
                ('fecha_creacion_eva', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion_eva', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
