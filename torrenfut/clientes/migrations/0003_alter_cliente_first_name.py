# Generated by Django 5.1.2 on 2024-10-17 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_alter_cliente_options_remove_cliente_cpf_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='first_name',
            field=models.CharField(default='-', max_length=50, verbose_name='nome'),
        ),
    ]
