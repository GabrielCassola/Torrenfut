# Generated by Django 5.1.2 on 2024-10-13 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_preco_camiseta_preco_custo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='camisetatamanho',
            name='estoque_minimo',
            field=models.IntegerField(default=5),
        ),
    ]