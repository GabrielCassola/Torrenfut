# Generated by Django 5.1.2 on 2024-10-17 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cliente',
            options={'ordering': ('first_name',), 'verbose_name': 'cliente', 'verbose_name_plural': 'clientes'},
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='cpf',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='nome',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='telefone',
        ),
        migrations.AddField(
            model_name='cliente',
            name='first_name',
            field=models.CharField(default='Desconhecido', max_length=50, verbose_name='nome'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='last_name',
            field=models.CharField(max_length=50, null=True, verbose_name='sobrenome'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
