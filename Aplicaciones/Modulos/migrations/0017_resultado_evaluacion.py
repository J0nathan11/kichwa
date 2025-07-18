# Generated by Django 4.1.13 on 2025-06-10 04:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Modulos', '0016_evaluacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resultado_Evaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota_res', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fecha_res', models.DateTimeField(auto_now_add=True)),
                ('fk_estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Modulos.estudiante')),
                ('fk_evaluacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Modulos.evaluacion')),
            ],
        ),
    ]
