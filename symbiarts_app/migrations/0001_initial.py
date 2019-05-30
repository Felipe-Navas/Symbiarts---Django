# Generated by Django 2.2 on 2019-05-25 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Obra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(blank=True, max_length=200)),
                ('stock', models.IntegerField(blank=True, default=0)),
                ('fecha_publicacion', models.DateField(verbose_name='Fecha de publicacion')),
                ('estado', models.CharField(choices=[('D', 'Denunciada'), ('N', 'Normal')], default='N', max_length=15)),
                ('dimensiones', models.CharField(blank=True, max_length=200)),
                ('precio', models.DecimalField(blank=True, decimal_places=2, max_digits=6)),
            ],
        ),
    ]
