# Generated by Django 3.1.5 on 2021-03-09 04:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prueba', '0004_auto_20210301_0204'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpcionPregunta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('fecha_creacion', models.DateField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('fecha_actualizacion', models.DateField(auto_now=True, verbose_name='Fecha de actualizacion')),
                ('fecha_eliminacion', models.DateField(auto_now=True, verbose_name='Fecha deeliminación')),
                ('contenido_opcion', models.CharField(max_length=250, unique=True, verbose_name='Contenido de la opción')),
                ('letra', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P')], max_length=1, unique=True, verbose_name='Letra')),
            ],
            options={
                'verbose_name': 'Opcion Enunciado',
                'verbose_name_plural': 'Opciones enunciado',
            },
        ),
        migrations.RemoveField(
            model_name='pregunta',
            name='opcion',
        ),
        migrations.AlterField(
            model_name='enunciadogrupopregunta',
            name='enunciado_general',
            field=models.TextField(unique=True, verbose_name='Enunciado general del grupo de preguntas'),
        ),
        migrations.AlterField(
            model_name='opcionrespuesta',
            name='letra_opcion',
            field=models.CharField(max_length=1, unique=True, verbose_name='nombre de la letra'),
        ),
        migrations.DeleteModel(
            name='OpcionEnunciado',
        ),
        migrations.AddField(
            model_name='opcionpregunta',
            name='pregunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prueba.pregunta'),
        ),
    ]
