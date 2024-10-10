# Generated by Django 5.1.2 on 2024-10-10 23:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fornecedores', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxa',
            name='tipo_produto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='taxas', to='fornecedores.tipoproduto'),
        ),
        migrations.AlterField(
            model_name='fornecedor',
            name='tipo_produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fornecedores.tipoproduto'),
        ),
    ]
