# Generated by Django 3.1.5 on 2021-09-09 03:10

from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Facultad',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('fecha_creacion', models.DateField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('fecha_actualizacion', models.DateField(auto_now=True, verbose_name='Fecha de actualizacion')),
                ('fecha_eliminacion', models.DateField(auto_now=True, verbose_name='Fecha deeliminación')),
                ('nombre_facultad', models.CharField(max_length=100, verbose_name='Nombre de la facultad')),
            ],
            options={
                'verbose_name': 'Facultad',
                'verbose_name_plural': 'Facultades',
                'ordering': ['nombre_facultad'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalFacultad',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('fecha_creacion', models.DateField(blank=True, editable=False, verbose_name='Fecha de creación')),
                ('fecha_actualizacion', models.DateField(blank=True, editable=False, verbose_name='Fecha de actualizacion')),
                ('fecha_eliminacion', models.DateField(blank=True, editable=False, verbose_name='Fecha deeliminación')),
                ('nombre_facultad', models.CharField(max_length=100, verbose_name='Nombre de la facultad')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical Facultad',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalNivelAcademico',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('fecha_creacion', models.DateField(blank=True, editable=False, verbose_name='Fecha de creación')),
                ('fecha_actualizacion', models.DateField(blank=True, editable=False, verbose_name='Fecha de actualizacion')),
                ('fecha_eliminacion', models.DateField(blank=True, editable=False, verbose_name='Fecha deeliminación')),
                ('nivel_academico', models.CharField(db_index=True, max_length=50, verbose_name='Nivel académico')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical Nivel academico',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalPrograma',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('fecha_creacion', models.DateField(blank=True, editable=False, verbose_name='Fecha de creación')),
                ('fecha_actualizacion', models.DateField(blank=True, editable=False, verbose_name='Fecha de actualizacion')),
                ('fecha_eliminacion', models.DateField(blank=True, editable=False, verbose_name='Fecha deeliminación')),
                ('nombre_programa', models.CharField(db_index=True, max_length=100, verbose_name='Nombre del programa')),
                ('creditos', models.PositiveSmallIntegerField(verbose_name='Creditos academicos del programa')),
                ('semestres', models.PositiveSmallIntegerField(verbose_name='Semetres')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical Programa',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSemestre',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('fecha_creacion', models.DateField(blank=True, editable=False, verbose_name='Fecha de creación')),
                ('fecha_actualizacion', models.DateField(blank=True, editable=False, verbose_name='Fecha de actualizacion')),
                ('fecha_eliminacion', models.DateField(blank=True, editable=False, verbose_name='Fecha deeliminación')),
                ('semestre', models.CharField(db_index=True, max_length=100, verbose_name='Semestre')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical Semestre',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='NivelAcademico',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('fecha_creacion', models.DateField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('fecha_actualizacion', models.DateField(auto_now=True, verbose_name='Fecha de actualizacion')),
                ('fecha_eliminacion', models.DateField(auto_now=True, verbose_name='Fecha deeliminación')),
                ('nivel_academico', models.CharField(max_length=50, unique=True, verbose_name='Nivel académico')),
            ],
            options={
                'verbose_name': 'Nivel academico',
                'verbose_name_plural': 'Niveles académicos',
                'ordering': ['nivel_academico'],
            },
        ),
        migrations.CreateModel(
            name='Semestre',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('fecha_creacion', models.DateField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('fecha_actualizacion', models.DateField(auto_now=True, verbose_name='Fecha de actualizacion')),
                ('fecha_eliminacion', models.DateField(auto_now=True, verbose_name='Fecha deeliminación')),
                ('semestre', models.CharField(max_length=100, unique=True, verbose_name='Semestre')),
            ],
            options={
                'verbose_name': 'Semestre',
                'verbose_name_plural': 'Semestres',
                'ordering': ['semestre'],
            },
        ),
        migrations.CreateModel(
            name='Programa',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('fecha_creacion', models.DateField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('fecha_actualizacion', models.DateField(auto_now=True, verbose_name='Fecha de actualizacion')),
                ('fecha_eliminacion', models.DateField(auto_now=True, verbose_name='Fecha deeliminación')),
                ('nombre_programa', models.CharField(max_length=100, unique=True, verbose_name='Nombre del programa')),
                ('creditos', models.PositiveSmallIntegerField(verbose_name='Creditos academicos del programa')),
                ('semestres', models.PositiveSmallIntegerField(verbose_name='Semetres')),
                ('facultad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institucional.facultad')),
            ],
            options={
                'verbose_name': 'Programa',
                'verbose_name_plural': 'Programas',
                'ordering': ['nombre_programa'],
            },
        ),
    ]
