# Generated by Django 5.1.2 on 2024-10-30 16:16

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_delete_historicoestoque'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricoEstoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField()),
                ('data_alteracao', models.DateTimeField(default=django.utils.timezone.now)),
                ('camiseta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historico_camisetas', to='store.camiseta')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historico_estoque', to='store.camisetatamanho')),
            ],
        ),
    ]
