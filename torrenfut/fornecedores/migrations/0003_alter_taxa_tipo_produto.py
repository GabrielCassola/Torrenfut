# Generated by Django 5.1.2 on 2024-10-10 23:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fornecedores', '0002_taxa_tipo_produto_alter_fornecedor_tipo_produto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxa',
            name='tipo_produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taxas', to='fornecedores.tipoproduto'),
        ),
    ]
