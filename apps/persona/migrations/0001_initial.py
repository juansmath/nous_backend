# Generated by Django 3.1.5 on 2021-09-09 03:10

from django.db import migrations, models
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalPersona',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('fecha_creacion', models.DateField(blank=True, editable=False, verbose_name='Fecha de creación')),
                ('fecha_actualizacion', models.DateField(blank=True, editable=False, verbose_name='Fecha de actualizacion')),
                ('fecha_eliminacion', models.DateField(blank=True, editable=False, verbose_name='Fecha deeliminación')),
                ('identificacion', models.PositiveIntegerField(db_index=True, verbose_name='Número de identificación')),
                ('primer_nombre', models.CharField(max_length=100, verbose_name='Primer nombre')),
                ('segundo_nombre', models.CharField(blank=True, max_length=100, null=True, verbose_name='Segundo nombre')),
                ('primer_apellido', models.CharField(max_length=100, verbose_name='Primer apellido')),
                ('segundo_apellido', models.CharField(blank=True, max_length=100, null=True, verbose_name='Segundo apellido')),
                ('genero', models.CharField(choices=[('F', 'FEMENINO'), ('M', 'MASCULINO'), ('LGTIB', 'LGTIB')], max_length=6, verbose_name='Genéro')),
                ('rh', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3, verbose_name='Grupo sanguineo')),
                ('estado_civil', models.CharField(choices=[('SOLTERO', 'SOLTERO(A)'), ('CASADO', 'CASADO'), ('DIVORCIADO', 'DIVORCIADO(A)'), ('VIUDO', 'VIUDO(A)'), ('UNION_LIBRE', 'UNION_LIBRE')], max_length=15, verbose_name='Estado civil')),
                ('telefono', models.CharField(db_index=True, max_length=50, verbose_name='Número de télefono')),
                ('fecha_nacimiento', models.DateField(verbose_name='Fecha de nacimiento')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical Persona',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('fecha_creacion', models.DateField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('fecha_actualizacion', models.DateField(auto_now=True, verbose_name='Fecha de actualizacion')),
                ('fecha_eliminacion', models.DateField(auto_now=True, verbose_name='Fecha deeliminación')),
                ('identificacion', models.PositiveIntegerField(unique=True, verbose_name='Número de identificación')),
                ('primer_nombre', models.CharField(max_length=100, verbose_name='Primer nombre')),
                ('segundo_nombre', models.CharField(blank=True, max_length=100, null=True, verbose_name='Segundo nombre')),
                ('primer_apellido', models.CharField(max_length=100, verbose_name='Primer apellido')),
                ('segundo_apellido', models.CharField(blank=True, max_length=100, null=True, verbose_name='Segundo apellido')),
                ('genero', models.CharField(choices=[('F', 'FEMENINO'), ('M', 'MASCULINO'), ('LGTIB', 'LGTIB')], max_length=6, verbose_name='Genéro')),
                ('rh', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3, verbose_name='Grupo sanguineo')),
                ('estado_civil', models.CharField(choices=[('SOLTERO', 'SOLTERO(A)'), ('CASADO', 'CASADO'), ('DIVORCIADO', 'DIVORCIADO(A)'), ('VIUDO', 'VIUDO(A)'), ('UNION_LIBRE', 'UNION_LIBRE')], max_length=15, verbose_name='Estado civil')),
                ('telefono', models.CharField(max_length=50, unique=True, verbose_name='Número de télefono')),
                ('fecha_nacimiento', models.DateField(verbose_name='Fecha de nacimiento')),
            ],
            options={
                'verbose_name': 'Persona',
                'verbose_name_plural': 'Personas',
                'ordering': ['primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido'],
            },
        ),
    ]
