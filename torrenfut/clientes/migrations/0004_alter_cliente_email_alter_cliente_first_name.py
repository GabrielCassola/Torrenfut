# Generated by Django 5.1.2 on 2024-10-18 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0003_alter_cliente_first_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='first_name',
            field=models.CharField(max_length=50, null=True, verbose_name='nome'),
        ),
    ]