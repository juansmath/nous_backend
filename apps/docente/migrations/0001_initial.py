# Generated by Django 3.1.5 on 2021-03-14 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institucional', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('fecha_creacion', models.DateField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('fecha_actualizacion', models.DateField(auto_now=True, verbose_name='Fecha de actualizacion')),
                ('fecha_eliminacion', models.DateField(auto_now=True, verbose_name='Fecha deeliminación')),
                ('nivel_academico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institucional.nivelacademico')),
            ],
            options={
                'verbose_name': 'Docente',
                'verbose_name_plural': 'Docentes',
            },
        ),
    ]
