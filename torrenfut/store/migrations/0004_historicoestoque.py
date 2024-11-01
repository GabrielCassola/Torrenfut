# Generated by Django 5.1.2 on 2024-10-30 00:55

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_camisetatamanho_estoque_minimo'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricoEstoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField()),
                ('data_alteracao', models.DateTimeField(default=django.utils.timezone.now)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.camisetatamanho')),
            ],
        ),
    ]
