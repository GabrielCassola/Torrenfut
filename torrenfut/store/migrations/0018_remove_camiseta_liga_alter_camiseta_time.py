# Generated by Django 5.1.2 on 2024-11-24 20:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_alter_camiseta_liga_alter_camiseta_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='camiseta',
            name='liga',
        ),
        migrations.AlterField(
            model_name='camiseta',
            name='time',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.time'),
        ),
    ]
